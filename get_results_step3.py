import os
import json
import requests
from pathlib import Path
import shutil
import random
import time


class StepfunEvaluator:
    def __init__(self, input_json_dir, output_base_dir):
        # 从环境变量获取API密钥
        self.api_key = "5ZMELfXpW5xQ15606tlcuJNWkab4LL2MkNYVqXRrg9OvZTNjXbrdqTEDyhhxFpyYP"
        self.input_json_dir = input_json_dir  # 输入JSON文件存放目录
        self.output_base_dir = output_base_dir  # 输出结果的基础目录
        # stepfun API地址
        self.base_url = "https://api.stepfun.com/v1/chat/completions"
        # 系统提示词，与提供的代码保持一致
        self.system_prompt = "You are an AI assistant, please answer the following questions based on the provided image. Don't show any reasoning processes. Answer each question directly and separately."# 使用stepfun的模型
        self.model_name = "step-1o-turbo-vision"

        # 创建输出目录（如果不存在）
        os.makedirs(self.output_base_dir, exist_ok=True)

    def _call_stepfun_api(self, pic_base64, questions):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 构造包含所有问题的文本
        questions_text = "\n".join([f"Question {i + 1}: {q}" for i, q in enumerate(questions)])
        full_prompt = f"{questions_text}\n\nPlease put each answer in a single line. Use this template exactly: <answer>\n<answer>\n.... DO NOT add any other symbol, number or word."

        # 构造消息，包含图片base64编码，使用stepfun要求的格式
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": full_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": pic_base64  # 这里假设pic_base64已经是完整的data URL
                        }
                    }
                ]
            }
        ]

        data = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.0
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            err_msg = f"API调用失败: {str(e)}"
            if "response" in locals():
                err_msg += f"，响应内容: {response.text}"
            print(err_msg)
            return None

    def process_single_file(self, json_path, difficulty_level):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 提取JSON中的关键信息
            pic_base64 = data.get("pic_base64", "")
            if not pic_base64:
                print(f"警告：文件 {json_path} 中未找到有效的pic_base64数据")
                return None

            # 确保图片是data URL格式，如果不是则转换
            if not pic_base64.startswith(("data:image/", "http://", "https://")):
                pic_base64 = f"data:image/png;base64,{pic_base64}"

            # 根据图类型构造问题、问题类型、正确答案列表
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

            # 打乱问题顺序
            combined = list(zip(questions, question_types, correct_answers))
            random.shuffle(combined)
            questions, question_types, correct_answers = zip(*combined)
            questions = list(questions)
            question_types = list(question_types)
            correct_answers = list(correct_answers)

            # 调用API
            model_responses = self._call_stepfun_api(pic_base64, questions)
            answers = []
            if model_responses:
                response_lines = [line.strip() for line in model_responses.split('\n') if line.strip()]
                for i in range(len(questions)):
                    if i < len(response_lines):
                        answers.append(response_lines[i])
                    else:
                        answers.append(f"未能解析第{i + 1}个问题的答案")
            else:
                answers = [f"API调用失败，未获取答案" for _ in range(len(questions))]

            # 打印结果
            print(f"\n处理文件: {json_path}")

            # 准备保存结果
            result_data = {
                "file_name": os.path.basename(json_path),
                "difficulty_level": difficulty_level + 1,
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

            # 保存结果
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
            print(f"在目录 {self.input_json_dir} 未找到符合条件的JSON文件（需以Graph开头、.json结尾）")
            return

        json_files.sort()
        total_count = len(json_files)
        results = []

        print(f"\n===== 开始处理难度等级 {difficulty_level + 1} 的文件 =====")
        for file in json_files:
            file_path = Path(self.input_json_dir) / file
            time.sleep(1)  # 简单限流
            result = self.process_single_file(file_path, difficulty_level)
            if result:
                results.append(result)

        print(f"\n===== 难度等级 {difficulty_level + 1} 处理完成 =====")
        print(f"共处理 {total_count} 个文件")
        return results


if __name__ == "__main__":
    graph_parent = "D:\\CVPR_code\\VGPE-Graph\\VGPE-base"
    input_json_dirs = [
        os.path.join(graph_parent, "Graph_level1"),
        os.path.join(graph_parent, "Graph_level2"),
        os.path.join(graph_parent, "Graph_level3")
    ]

    output_base_dir = "D:\\CVPR_code\\Stepfun_answer"  # 结果输出目录
    # 不再直接在这里设置API_KEY，而是从环境变量获取

    # 清除并重建输出目录（可选）
    if os.path.exists(output_base_dir):
        shutil.rmtree(output_base_dir)

    # 按难度等级处理
    all_results = []
    for level in range(len(input_json_dirs)):
        input_dir = input_json_dirs[level]
        evaluator = StepfunEvaluator(
            input_json_dir=input_dir,
            output_base_dir=output_base_dir
        )
        level_results = evaluator.run_processing(level)
        all_results.append(level_results)

    print("\n===== 所有处理完成 =====")
