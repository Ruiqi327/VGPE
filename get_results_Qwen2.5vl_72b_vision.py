import os
import json
import re
import requests
from pathlib import Path
import shutil
import time
import random
import string



class QwenVLEvaluator:
    def __init__(self, api_key, api_secret, input_json_dir, output_base_dir, region="cn-beijing"):
        self.api_key = api_key  # Qwen API密钥
        self.api_secret = api_secret  # Qwen API密钥对应的secret
        self.input_json_dir = input_json_dir  # 输入JSON文件存放目录
        self.output_base_dir = output_base_dir  # 输出结果的基础目录
        self.region = region  # 地域，如cn-beijing、cn-hangzhou等
        # Qwen2.5VL的API端点（通义千问API）
        self.base_url = f"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        self.system_prompt = "You are an AI assistant, please answer the following questions based on the provided image. Don't show any reasoning processes. Answer each question directly and separately."
        self.model_name = "qwen2.5-vl-72b-instruct"  # Qwen2.5VL的模型名称（根据实际版本调整）

        # 创建输出目录（如果不存在）
        os.makedirs(self.output_base_dir, exist_ok=True)

    def _get_access_token(self):
        return self.api_key


    def _call_qwen_api(self, pic_base64, questions):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_access_token()}" 
        }

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": [] 
            }
        ]

        if pic_base64:
            # 确保base64字符串不带前缀，此处补充完整格式
            if not pic_base64.startswith("data:image"):
                pic_base64 = f"data:image/png;base64,{pic_base64}"
            messages[1]["content"].append({
                "type": "image_url",
                "image_url": pic_base64
            })

        # 再添加问题文本
        questions_text = "\n".join([f"Question {i + 1}: {q}" for i, q in enumerate(questions)])
        messages[1]["content"].append({
            "type": "text",
            "text": f"{questions_text}\n\nPlease put each answer in a single line. Use this template exactly: <answer>\n<answer>\n.... DO NOT add any other symbol, number or word.",
        })

        data = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.0
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()

            # 解析Qwen的响应（结构与OpenAI兼容，但需确认）
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"Qwen API返回格式异常: {result}")
                return None
        except Exception as e:
            print(f"Qwen API调用失败: {str(e)}，响应内容: {response.text if 'response' in locals() else '无响应'}")
            return None

    def process_single_file(self, json_path, difficulty_level):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 提取关键信息
            pic_base64 = data.get("pic_base64", "")  # 图片base64编码
            pic_layout = data.get("pic_layout", "")
            if not pic_base64:
                print(f"警告：文件 {json_path} 中未找到有效的pic_base64数据")

            # 问题列表（保持原有逻辑不变）
            if data["direct_answer"] == "No" and data["weight_answer"] == "No":  # 无向无权图
                questions = [
                    data["node_question1"],
                    data["node_question2"],
                    data["node_question3"],
                    data["direct_question"],
                    data["weight_question"],
                    data["edge_question1"],
                    data["edge_question2"],
                    data["edge_question3"]
                ]
                question_types = [
                    "node_question1","node_question2", "node_question3","direct_question", "weight_question",
                    "edge_question1", "edge_question2", "edge_question3"
                ]
                correct_answers = [
                    data["node_answer1"], data["node_answer2"],data["node_answer3"], data["direct_answer"], data["weight_answer"],
                    data["edge_answer1"], data["edge_answer2"],data["edge_answer3"]
                ]
            elif data["direct_answer"] == "No" and data["weight_answer"] == "Yes":  # 无向有权图
                questions = [
                    data["node_question1"],
                    data["node_question2"],  data["node_question3"], data["direct_question"], data["weight_question"],
                    data["query_weight1"], data["query_weight2"],data["query_weight3"], data["edge_question1"], data["edge_question2"],data["edge_question3"]
                ]
                question_types = [
                    "node_question1","node_question2","node_question3", "direct_question", "weight_question",
                    "query_weight1", "query_weight2", "query_weight3", "edge_question1", "edge_question2", "edge_question3"
                ]
                correct_answers = [
                    data["node_answer1"], data["node_answer2"], data["node_answer3"], data["direct_answer"], data["weight_answer"],
                    data["answer_weight1"], data["answer_weight2"], data["answer_weight3"], data["edge_answer1"], data["edge_answer2"], data["edge_answer3"]
                ]
            elif data["direct_answer"] == "Yes" and data["weight_answer"] == "No":  # 有向无权图
                questions = [
                    data["node_question1"],
                    data["node_question2"],data["node_question3"], data["direct_question"], data["weight_question"],
                    data["query_point1"], data["query_point2"], data["query_point3"],data["edge_question1"], data["edge_question2"],data["edge_question3"]
                ]
                question_types = [
                    "node_question1","node_question2", "node_question3",  "direct_question", "weight_question",
                    "query_point1", "query_point2","query_point3", "edge_question1", "edge_question2","edge_question3"
                ]
                correct_answers = [
                    data["node_answer1"], data["node_answer2"], data["node_answer3"], data["direct_answer"], data["weight_answer"],
                    data["answer_point1"], data["answer_point2"],data["answer_point3"], data["edge_answer1"], data["edge_answer2"],data["edge_answer3"]
                ]
            else:  # 有向有权图
                questions = [
                    data["node_question1"],
                    data["node_question2"],   data["node_question3"], data["direct_question"], data["weight_question"],
                    data["query_weight1"], data["query_weight2"],data["query_weight3"],
                    data["query_point1"], data["query_point2"],data["query_point3"],
                    data["edge_question1"], data["edge_question2"], data["edge_question3"]
                ]

                question_types = [
                    "node_question1","node_question2","node_question3", "direct_question", "weight_question",
                    "query_weight1", "query_weight2","query_weight3",
                    "query_point1", "query_point2","query_point3",
                    "edge_question1", "edge_question2", "edge_question3"
                ]
                correct_answers = [
                    data["node_answer1"], data["node_answer2"],data["node_answer3"],
                    data["direct_answer"], data["weight_answer"],
                    data["answer_weight1"], data["answer_weight2"],data["answer_weight3"],
                    data["answer_point1"], data["answer_point2"],data["answer_point3"],
                    data["edge_answer1"], data["edge_answer2"],data["edge_answer3"]
                ]

            combined = list(zip(questions, question_types, correct_answers))
            # 2. 打乱元组列表的顺序
            random.shuffle(combined)
            # 3. 拆分打乱后的元组列表，还原成三个列表（保持对应关系）
            questions, question_types, correct_answers = zip(*combined)
            # 4. 转换为列表类型（zip返回的是元组，按需转换）
            questions = list(questions)
            question_types = list(question_types)
            correct_answers = list(correct_answers)
            # 调用Qwen API
            model_responses = self._call_qwen_api(pic_base64, questions)
            # 解析答案（逻辑不变）

            answers = []

            if model_responses:
                # 分割响应为行列表，过滤空行
                response_lines = [line.strip() for line in model_responses.split('\n') if line.strip()]
                for i in range(len(questions)):
                    # 直接按顺序取对应行作为答案，超出行数则标记未找到
                    if i < len(response_lines):
                        answers.append(response_lines[i])
                    else:
                        answers.append(f"未能解析第{i + 1}个问题的答案")
            else:
                answers = [f"API调用失败，未获取答案" for _ in range(len(questions))]


            # 打印结果
            print(f"\n处理文件: {json_path}")

            # 保存结果
            result_data = {
                "file_name": os.path.basename(json_path),
                "difficulty_level": difficulty_level+1,
                "results": []
            }

            for i in range(len(questions)):
                result_data["results"].append({
                    "question_type": question_types[i],
                    "question": questions[i],
                    "model_answer": answers[i],
                    "correct_answer": correct_answers[i],
                    "is_correct": correct_answers[i] in answers[i]
                })

            output_dir = os.path.join(self.output_base_dir, f"level_{difficulty_level + 1}")
            os.makedirs(output_dir, exist_ok=True)
            output_filename = f"results_{os.path.basename(json_path)}"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            return result_data

        except Exception as e:
            print(f"{json_path}：处理失败({str(e)})")
            return None

    def run_processing(self, difficulty_level):
        json_files = [f for f in os.listdir(self.input_json_dir)
                      if f.startswith("Graph") and f.endswith(".json")]

        if not json_files:
            print(f"在目录 {self.input_json_dir} 未找到符合条件的JSON文件")
            return

        json_files.sort()
        total_count = len(json_files)
        results = []

        print(f"\n===== 开始处理难度等级 {difficulty_level + 1} 的文件 =====")

        for file in json_files:
            file_path = Path(self.input_json_dir) / file
            # 调用API时添加延迟，避免触发限流
            time.sleep(0.5)  # 根据Qwen API的限流规则调整
            result = self.process_single_file(file_path, difficulty_level)
            if result:
                results.append(result)

        print(f"\n===== 难度等级 {difficulty_level + 1} 处理完成 =====")
        print(f"共处理 {total_count} 个文件")
        return results


if __name__ == "__main__":
    graph_parent = " "
    input_json_dirs = [
        os.path.join(graph_parent, "Graph_level1"),
        os.path.join(graph_parent, "Graph_level2"),
        os.path.join(graph_parent, "Graph_level3")
    ]

    output_base_dir = " "  # 输出目录
    # 以下为需要您提供的Qwen2.5VL相关信息
    QWEN_API_KEY = " "  # 替换为您的Qwen API Key
    QWEN_API_SECRET = "your_qwen_api_secret"  # 替换为您的Qwen API Secret（如不需要可留空）
    QWEN_REGION = "cn-beijing"  # 替换为您的API地域（如cn-hangzhou）

    # 清除并重建输出目录
    if os.path.exists(output_base_dir):
        shutil.rmtree(output_base_dir)

    # 按难度等级处理
    all_results = []
    for level in range(len(input_json_dirs)):
        input_dir = input_json_dirs[level]
        evaluator = QwenVLEvaluator(
            api_key=QWEN_API_KEY,
            api_secret=QWEN_API_SECRET,
            input_json_dir=input_dir,
            output_base_dir=output_base_dir,
            region=QWEN_REGION
        )
        level_results = evaluator.run_processing(level)
        all_results.append(level_results)


    print("\n===== 所有处理完成 =====")
