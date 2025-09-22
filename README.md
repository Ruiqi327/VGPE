# VGPE: A Visual Graph Perception Evaluation Benchmark

## Access of VGPE dataset
https://pan.quark.cn/s/65c71c8780b7
This dataset contains VGPE-base, -edge, -layout, -node, -color and VGPE-base-tiny for GPT-4.1.

## Task Templates
NC: Please answer the following question only with Yes or No, do not add any other words. Does Node " + str(index) + " exist in this graph?\\
DGC: Please answer the following question only with Yes or No, do not add any other words. Is this graph directed?\\
WGC: Please answer the following question only with Yes or No, do not add any other words. Is this graph weighted?\\
EC: Please answer the following question only with Yes or No, do not add any other words. Without distinguishing the direction of edges, is there an edge between Node " + str(index1) + " and Node " + str(index2) + "?\\
DQ: Regardless of direction, please check if there is any edge between Node "+str(index1)+" and Node "+str(index2)+", if you don't see any edge between them, please only answer 0. If there is an edge, then answer Yes if Node "+str(index1)+" points to         Node "+str(index2)+", otherwise answer No. Do not add any other words.\\
WQ: Please answer the following question with only one number, do not add any other words. Without distinguishing the direction of edges, what is the weight of the edge connecting Node "+str(index1)+" with Node "+str(index2)+"? If you don't see any edge      between them, please only answer 0.

## Examples of VGPE-node, -edge, -layout and -color.
### VGPE-node (Tiny,small,Big)
<img width="300" height="575" alt="image" src="https://github.com/user-attachments/assets/723028a9-271d-420a-b8b7-b5631468aa73" />
<img width="200" height="728" alt="image" src="https://github.com/user-attachments/assets/ea508c4a-e86b-4747-bbc4-5b677fe6774a" />
<img width="300" height="1606" alt="image" src="https://github.com/user-attachments/assets/d2a8e2aa-5d2d-46c8-a103-38123cc52a07" />                                            

### VGPE-edge (Half, double, triple)
<img width="300" height="1019" alt="image" src="https://github.com/user-attachments/assets/2a065389-dd53-4960-9016-2f15e8b10aca" />
<img width="300" height="800" alt="image" src="https://github.com/user-attachments/assets/783fbce6-8083-4f6f-a9cf-03dd804c7082" />
<img width="200" height="1458" alt="image" src="https://github.com/user-attachments/assets/50378ea9-e4bc-4898-abbb-4d99c9d81402" />

### VGPE-layout (Neato, twopi, circo)
<img width="250" height="1366" alt="image" src="https://github.com/user-attachments/assets/e72c4c9c-1611-4f2f-99b9-83800ac3826e" />
<img width="250" height="1142" alt="image" src="https://github.com/user-attachments/assets/51634be6-cc3f-4d60-b2c7-6bfa1009ea0c" />
<img width="250" height="1054" alt="image" src="https://github.com/user-attachments/assets/9242f5c5-063b-468a-9ea3-9a55222060b7" />

### VGPE-color (Red, green, blue, mixed)
<img width="150" height="1239" alt="image" src="https://github.com/user-attachments/assets/b8709f15-2c46-498a-a609-26397914e618" />
<img width="150" height="1239" alt="image" src="https://github.com/user-attachments/assets/19bafa58-b6e2-4af6-9645-e9b5b499123e" />
<img width="150" height="1239" alt="image" src="https://github.com/user-attachments/assets/f0505a52-4935-4a72-a44a-7a9bf256f2a3" />
<img width="300" height="1138" alt="image" src="https://github.com/user-attachments/assets/66c96b24-92ad-47ee-bbb7-a3d173a46eca" />


