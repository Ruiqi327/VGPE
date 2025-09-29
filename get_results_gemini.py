import os
import json
from pathlib import Path
import shutil
import random
import time
from openai import OpenAI
from openai import OpenAIError

class OpenAIEvaluator:
    def __init__(self, input_json_dir, output_base_dir):
        self.api_key =r''
        if not self.api_key:
            raise ValueError("请设置环境变量 'OPENAI_API_KEY'（OpenAI密钥）")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=''
        )
        self.input_json_dir = input_json_dir
        self.output_base_dir = output_base_dir
        self.model_name = "gemini-2.5-flash-lite"
        self.system_prompt = "You are an AI assistant, please answer the following questions based on the provided image. Don't show any reasoning processes. Answer each question directly and separately."

        os.makedirs(self.output_base_dir, exist_ok=True)

    def _call_openai_api(self, pic_url, questions):
        try:
            questions_text = "\n".join([f"Question {i + 1}：{q}" for i, q in enumerate(questions)])
            full_prompt = f"{questions_text}\n\nPlease put each answer in a single line. Use this template exactly: <answer>\n<answer>\n.... DO NOT add any other symbol, number or word."
            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": pic_url,
                                "detail": "high"
                            }
                        },
                        {"type": "text", "text":full_prompt}
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.0,  # 固定输出，确保测评一致性
                timeout=120
            )

            return response.choices[0].message.content.strip()

        except ImportError:
            print("错误：请安装openai库（pip install openai）")
            return None
        except OpenAIError as e:
            err_msg = f"API调用失败: {str(e)}"
            if hasattr(e, 'response'):
                err_msg += f"，响应状态: {e.response.status_code}"
            print(err_msg)
            return None
        except Exception as e:
            print(f"处理错误: {str(e)}")
            return None

    def process_single_file(self, json_path, difficulty_level):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            pic_base64 = data.get("pic_base64", "")
            if not pic_base64:
                print(f"警告：{json_path} 缺少pic_base64数据")
                return None

            if not pic_base64.startswith(("data:image/", "http://", "https://")):
                pic_base64 = f"data:image/png;base64,{pic_base64}"

            if data["direct_answer"] == "No" and data["weight_answer"] == "No":
                questions = [data["node_question1"], data["node_question2"], data["node_question3"],
                             data["direct_question"], data["weight_question"],
                             data["edge_question1"], data["edge_question2"], data["edge_question3"]]
                question_types = ["node_question1", "node_question2", "node_question3",
                                  "direct_question", "weight_question",
                                  "edge_question1", "edge_question2", "edge_question3"]
                correct_answers = [data["node_answer1"], data["node_answer2"], data["node_answer3"],
                                   data["direct_answer"], data["weight_answer"],
                                   data["edge_answer1"], data["edge_answer2"], data["edge_answer3"]]
            elif data["direct_answer"] == "No" and data["weight_answer"] == "Yes":
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
            elif data["direct_answer"] == "Yes" and data["weight_answer"] == "No":
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
            else:
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

            # 打乱问题顺序
            combined = list(zip(questions, question_types, correct_answers))
            random.shuffle(combined)
            questions, question_types, correct_answers = zip(*combined)
            questions = list(questions)
            question_types = list(question_types)
            correct_answers = list(correct_answers)

            # 调用API
            model_responses = self._call_openai_api(pic_base64, questions)
            answers = []
            if model_responses:
                response_lines = [line.strip() for line in model_responses.split('\n') if line.strip()]
                for i in range(len(questions)):
                    answers.append(response_lines[i] if i < len(response_lines)
                                   else f"未能解析第{i + 1}个问题的答案")
            else:
                answers = [f"API调用失败，未获取答案" for _ in range(len(questions))]

            print(f"\n处理文件: {json_path}")

            # 保存结果
            result_data = {
                "file_name": os.path.basename(json_path),
                "difficulty_level": difficulty_level + 1,
                "results": [
                    {
                        "question_type": question_types[i],
                        "question": questions[i],
                        "model_answer": answers[i],
                        "correct_answer": correct_answers[i],
                        "is_correct": correct_answers[i] in answers[i]
                    } for i in range(len(questions))
                ]
            }

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
            time.sleep(0.5)
            result = self.process_single_file(file_path, difficulty_level)
            if result:
                results.append(result)

        print(f"\n===== 难度等级 {difficulty_level + 1} 处理完成 =====")
        print(f"共处理 {total_count} 个文件，成功 {len(results)} 个")
        return results


if __name__ == "__main__":
    graph_parent = ""
    input_json_dirs = [
        os.path.join(graph_parent, "Graph_level1"),
        os.path.join(graph_parent, "Graph_level2"),
        os.path.join(graph_parent, "Graph_level3")
    ]
    output_base_dir = ""

    if os.path.exists(output_base_dir):
        shutil.rmtree(output_base_dir)

    all_results = []
    for level in range(len(input_json_dirs)):
        evaluator = OpenAIEvaluator(
            input_json_dir=input_json_dirs[level],
            output_base_dir=output_base_dir
        )
        level_results = evaluator.run_processing(level)
        all_results.append(level_results)


    print("\n===== 所有难度等级处理完成 =====")
