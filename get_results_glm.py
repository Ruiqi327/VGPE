import os
import json
from pathlib import Path
import shutil
import random
import time
# 1. 引入GLM所需的ZhipuAiClient
from zai import ZhipuAiClient


class GLMEvaluator:
    def __init__(self, input_json_dir, output_base_dir):
        self.api_key = r"c4d01b68ff3b4c819118ff198251ffc2.EGYQNlMVY6ippT2A"
        self.client = ZhipuAiClient(api_key=self.api_key)
        self.input_json_dir = input_json_dir
        self.output_base_dir = output_base_dir
        self.model_name = "glm-4.5v"
        self.system_prompt = "You are an AI assistant, please answer the following questions based on the provided image. Don't show any reasoning processes. Answer each question directly and separately."
        os.makedirs(self.output_base_dir, exist_ok=True)

    def _call_glm_api(self, pic_url, questions):
        try:
            # 构造问题文本：按序号整理所有问题（原逻辑保留）
            questions_text = "\n".join([f"Question {i + 1}：{q}" for i, q in enumerate(questions)])
            full_prompt = f"{questions_text}\n\nPlease put each answer in a single line. Use this template exactly: <answer>\n<answer>\n.... DO NOT add any other symbol, number or word."
            messages = [
                {"role": "system", "content": self.system_prompt},
                # user消息：包含图片URL和问题集合
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": pic_url}
                        },
                        # 文本对象（所有问题）
                        {"type": "text", "text": full_prompt}
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                thinking={"type": "disabled"},  # 启用深度思考（与参考GLM调用一致）
                timeout=120  #
            )

            # 解析响应：提取模型回答（GLM的响应结构）
            return response.choices[0].message.content.strip()

        except ImportError:
            print("错误：未找到 'zai' 库，请执行 'pip install zai' 安装GLM客户端依赖")
            return None
        except Exception as e:
            err_msg = f"GLM API调用失败: {str(e)}"
            # 若有响应对象，补充响应信息
            if "response" in locals() and hasattr(response, "text"):
                err_msg += f"，响应内容: {response.text}"
            print(err_msg)
            return None

    def process_single_file(self, json_path, difficulty_level):
        """5. 保留原业务逻辑：读取JSON、构造问题、解析结果、保存输出"""
        try:
            # 读取输入JSON文件（原逻辑不变）
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 提取图片数据：处理base64格式（GLM支持data URL或公网URL）
            pic_base64 = data.get("pic_base64", "")
            if not pic_base64:
                print(f"警告：文件 {json_path} 中未找到有效的pic_base64数据")
                return None

            # 格式处理：若为纯base64字符串，补充data URL前缀（确保GLM识别）
            if not pic_base64.startswith(("data:image/", "http://", "https://")):
                pic_base64 = f"data:image/png;base64,{pic_base64}"

            # 按图片类型构造问题、问题类型、正确答案（原逻辑完全保留）
            if data["direct_answer"] == "No" and data["weight_answer"] == "No":  # 无向无权图
                questions = [data["node_question1"], data["node_question2"], data["node_question3"],
                             data["direct_question"], data["weight_question"],
                             data["edge_question1"], data["edge_question2"], data["edge_question3"]]
                question_types = ["node_question1", "node_question2", "node_question3",
                                  "direct_question", "weight_question",
                                  "edge_question1", "edge_question2", "edge_question3"]
                correct_answers = [data["node_answer1"], data["node_answer2"], data["node_answer3"],
                                   data["direct_answer"], data["weight_answer"],
                                   data["edge_answer1"], data["edge_answer2"], data["edge_answer3"]]
            elif data["direct_answer"] == "No" and data["weight_answer"] == "Yes":  # 无向有权图
                questions = [data["node_question1"], data["node_question2"], data["node_question3"],
                             data["direct_question"], data["weight_question"],
                             data["query_weight1"], data["query_weight2"], data["query_weight3"],
                             data["edge_question1"], data["edge_question2"], data["edge_question3"]]
                question_types = ["node_question1", "node_question2", "node_question3",
                                  "direct_question", "weight_question",
                                  "query_weight1", "query_weight2", "query_weight3",
                                  "edge_question1", "edge_question2", "edge_question3"]
                correct_answers = [data["node_answer1"], data["node_answer2"], data["node_answer3"],
                                   data["direct_answer"], data["weight_answer"],
                                   data["answer_weight1"], data["answer_weight2"], data["answer_weight3"],
                                   data["edge_answer1"], data["edge_answer2"], data["edge_answer3"]]
            elif data["direct_answer"] == "Yes" and data["weight_answer"] == "No":  # 有向无权图
                questions = [data["node_question1"], data["node_question2"], data["node_question3"],
                             data["direct_question"], data["weight_question"],
                             data["query_point1"], data["query_point2"], data["query_point3"],
                             data["edge_question1"], data["edge_question2"], data["edge_question3"]]
                question_types = ["node_question1", "node_question2", "node_question3",
                                  "direct_question", "weight_question",
                                  "query_point1", "query_point2", "query_point3",
                                  "edge_question1", "edge_question2", "edge_question3"]
                correct_answers = [data["node_answer1"], data["node_answer2"], data["node_answer3"],
                                   data["direct_answer"], data["weight_answer"],
                                   data["answer_point1"], data["answer_point2"], data["answer_point3"],
                                   data["edge_answer1"], data["edge_answer2"], data["edge_answer3"]]
            else:  # 有向有权图
                questions = [data["node_question1"], data["node_question2"], data["node_question3"],
                             data["direct_question"], data["weight_question"],
                             data["query_weight1"], data["query_weight2"], data["query_weight3"],
                             data["query_point1"], data["query_point2"], data["query_point3"],
                             data["edge_question1"], data["edge_question2"], data["edge_question3"]]
                question_types = ["node_question1", "node_question2", "node_question3",
                                  "direct_question", "weight_question",
                                  "query_weight1", "query_weight2", "query_weight3",
                                  "query_point1", "query_point2", "query_point3",
                                  "edge_question1", "edge_question2", "edge_question3"]
                correct_answers = [data["node_answer1"], data["node_answer2"], data["node_answer3"],
                                   data["direct_answer"], data["weight_answer"],
                                   data["answer_weight1"], data["answer_weight2"], data["answer_weight3"],
                                   data["answer_point1"], data["answer_point2"], data["answer_point3"],
                                   data["edge_answer1"], data["edge_answer2"], data["edge_answer3"]]

            # 打乱问题顺序（原逻辑保留，确保评估随机性）
            combined = list(zip(questions, question_types, correct_answers))
            random.shuffle(combined)
            questions, question_types, correct_answers = zip(*combined)
            questions = list(questions)
            question_types = list(question_types)
            correct_answers = list(correct_answers)

            # 调用GLM API获取答案
            model_responses = self._call_glm_api(pic_base64, questions)
            answers = []
            if model_responses:
                # 分割响应：按行提取每个问题的答案（与原逻辑一致）
                response_lines = [line.strip() for line in model_responses.split('\n') if line.strip()]
                for i in range(len(questions)):
                    answers.append(response_lines[i] if i < len(response_lines)
                                   else f"未能解析第{i + 1}个问题的答案")
            else:
                answers = [f"API调用失败，未获取答案" for _ in range(len(questions))]

            # 打印处理进度（原逻辑保留）
            print(f"\n处理文件: {json_path}")

            # 构造结果数据（原逻辑保留，用于保存）
            result_data = {
                "file_name": os.path.basename(json_path),
                "difficulty_level": difficulty_level + 1,
                "results": [
                    {
                        "question_type": question_types[i],
                        "question": questions[i],
                        "model_answer": answers[i],
                        "correct_answer": correct_answers[i],
                        "is_correct": correct_answers[i] in answers[i]  # 正确性判断
                    } for i in range(len(questions))
                ]
            }

            # 保存结果到输出目录（原逻辑保留）
            output_dir = os.path.join(self.output_base_dir, f"level_{difficulty_level + 1}")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"results_{os.path.basename(json_path)}")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)

            return result_data

        except Exception as e:
            print(f"{json_path}：处理失败({str(e)})")
            return None

    def run_processing(self, difficulty_level):
        """6. 批量处理指定难度等级的文件（原逻辑保留）"""
        # 筛选符合条件的JSON文件（Graph开头、.json结尾）
        json_files = [f for f in os.listdir(self.input_json_dir)
                      if f.startswith("Graph") and f.endswith(".json")]
        if not json_files:
            print(f"在目录 {self.input_json_dir} 未找到符合条件的JSON文件")
            return

        # 按序号排序文件
        json_files.sort()
        total_count = len(json_files)
        results = []

        # 批量处理每个文件
        print(f"\n===== 开始处理难度等级 {difficulty_level + 1} 的文件 =====")
        for file in json_files:
            file_path = Path(self.input_json_dir) / file
            time.sleep(0.2)  # 简单限流，避免API请求过于密集
            result = self.process_single_file(file_path, difficulty_level)
            if result:
                results.append(result)

        print(f"\n===== 难度等级 {difficulty_level + 1} 处理完成 =====")
        print(f"共处理 {total_count} 个文件，成功 {len(results)} 个")
        return results


if __name__ == "__main__":
    # 7. 执行入口（原路径逻辑保留，调整输出目录）
    graph_parent = "D:\\CVPR_code\\VGPE-Graph\\VGPE-base"
    input_json_dirs = [
        os.path.join(graph_parent, "Graph_level1"),
        os.path.join(graph_parent, "Graph_level2"),
        os.path.join(graph_parent, "Graph_level3")
    ]
    output_base_dir = "D:\\CVPR_code\\GLM_answer"  # GLM结果输出目录

    # 清除旧输出目录（可选，原逻辑保留）
    if os.path.exists(output_base_dir):
        shutil.rmtree(output_base_dir)

    # 按难度等级批量处理
    all_results = []
    for level in range(len(input_json_dirs)):
        evaluator = GLMEvaluator(
            input_json_dir=input_json_dirs[level],
            output_base_dir=output_base_dir
        )
        level_results = evaluator.run_processing(level)
        all_results.append(level_results)

    print("\n===== 所有难度等级处理完成 =====")