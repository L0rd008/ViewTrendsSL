https://arxiv.org/html/2503.04446v1


License: arXiv.org perpetual non-exclusive license
arXiv:2503.04446v1 [cs.SI] 06 Mar 2025
SMTPD: A New Benchmark for Temporal Prediction of Social Media Popularity
1Yijie Xu*, 1Bolun Zheng*†, 1Wei Zhu*, 1Hangjia Pan, 1Yuchen Yao,
2Ning Xu, 2Anan Liu, 3Quan Zhang, 1Chenggang Yan
1Hangzhou Dianzi University, 2Tianjin University, 3Peking University
Abstract
Social media popularity prediction task aims to predict the popularity of posts on social media platforms, which has a positive driving effect on application scenarios such as content optimization, digital marketing and online advertising. Though many studies have made significant progress, few of them pay much attention to the integration between popularity prediction with temporal alignment. In this paper, with exploring YouTube’s multilingual and multi-modal content, we construct a new social media temporal popularity prediction benchmark, namely SMTPD, and suggest a baseline framework for temporal popularity prediction. Through data analysis and experiments, we verify that temporal alignment and early popularity play crucial roles in social media popularity prediction for not only deepening the understanding of temporal dynamics of popularity in social media but also offering a suggestion about developing more effective prediction models in this field. Code is available at https://github.com/zhuwei321/SMTPD

12†
1Introduction
With the advancement of Internet communication technology in recent years, social media has gradually emerged and has influenced various aspects of human life. Any content posted on social media stands the chance of becoming hot spot, and widely disseminated social media content can generate significant social and economic benefits. The prediction of social media popularity holds immense potential applications in content optimization [1, 30], online advertising [15, 14], digital marketing [19, 45], search recommendations [17, 4], intelligent fashion [10], and beyond.

Refer to caption
(a)
Refer to caption
(b)
Figure 1:Content sections and popularity trend of SMTPD. In 1(a), a sample involves four sections of content, with temporal popularity. 1(b) depicts box plots of daily popularity scores, illustrating variations in popularity distribution at different time points. The distribution consistently demonstrates a decay pattern over time.
In the early stages of popularity research, statistical and topological methods [43, 53, 41] were extensively employed, with the research focus primarily on time-aware popularity prediction. These prediction methods rely on information about the earlier popularity of posted content. Along with the many large-scale social media popularity datasets are proposed [3, 42, 47, 48], the machine learning based methods are widely employed to achieve reasonable predictions of social media popularity and have shown remarkable performance. These methods emphasize meticulous design in feature extraction and fusion, followed by popularity prediction using machine learning models such as deep neural networks (DNN) and gradient boosting decision trees (GBDT).

Table 1 lists the public or mentioned social media popularity datasets in the most recent years as far as we know. For above machine learning based methods, the large-scale social media popularity datasets [3, 35, 42, 47, 48, 11] provide the fundamental supports.

However, existing datasets and related studies have notable limitations, such as insufficient multi-modal data, limited language diversity, and, crucially, the absence of a consistent timeline for prediction. As shown in Figure1(b), popularity distributions shift over time, and predictions made at irregular intervals can reduce accuracy and create challenges for practical applications.

Dataset	Source	Category	Samples	Language	Prediction Type
Mazloom [35] 	Instagram	fast food brand	75K	English	single
Sanjo [42] 	Cookpad	recipe	150K	Japanese	single
TPIC17 [47] 	Flickr	-	680K	English	single
SMPD [48] 	Flickr	11 categories	486K	English	single
AMPS [11] 	YouTube	shorts	13K	Korean	single
SMTPD (ours)	YouTube	15 categories	282K	over 90 languages	sequential
 
Table 1:Comparing SMTPD with existed multi-modal social media popularity datasets.
Furthermore, effective popularity prediction requires integrating both the multi-modal content of social media and information on the communication process to capture the dynamic trends in popularity. This essential aspect is missing in most current prediction efforts.

Targeting to fix up the above shortcomings of existed datasets, in this paper, we propose a new benchmark called Social Media Temporal Popularity Dataset (SMTPD) by observing multi-modal content from mainstream for cutting-edge research in the field of social multimedia along with multi-modal feature temporal prediction. As shown in Figure 1(a), multi-modal contents of social media posts in multiple languages generated the daily popularity information during the communication process. We define such a post as a sample of SMTPD, and propose a multi-modal framework as a baseline to achieve the temporal prediction of popularity scores.The proposed framework consists of two parts, feature extraction and regression. In the feature extraction part, multiple pre-training models and pre-processing methods are introduced to translate the multi-modal content into deep features. In the regression part, we encode the state and time sequence of the extracted features, and adopt the LSTM-based structure to regress the 30-day popularities. Through analysis and experiments, we discover the importance of early popularity to the task of popularity prediction, and demonstrate the effectiveness of our method in temporal prediction. Generally, the contribution of this work can be summarized as:

• Against the missing of temporal information in social media popularity researches, we observe over 282K multilingual samples from mainstream social media since they released on the network lasting for 30 days. We refer to these samples as SMTPD, a new benchmark for temporal popularity prediction.
• Basing on existed methods, we innovate in both the selection of feature extractors and the construction of the temporal regression component, and suggest a baseline model which enables temporal popularity prediction to be conducted across multiple languages while aligning prediction times.
• Exploring the popularity distribution and the correlation between popularity at different times. Based on these, We find the importance of early popularity for popularity prediction task, and point out that the key-point for predicting popularity is to accurately predict the early popularity.
2Related work
Statistical and topological methods. Szabo et al. [43] found that the early-stage popularity notably influences subsequent popularity. Yang et al. [53] conducted cluster analysis on temporal patterns within online content, revealing distinct characteristics of popularity variations across different clusters. Richier et al. [41, 40] proposes bio-inspired models to characterize the evolution of video view counts. Wu et al. [51] suggested that the information cascade process is best described as an activate–decay dynamic process.

Multi-modal feature based Methods. Ding et al. [13] use pre-trained ResNet and BERT to extract visual and textual features, with the DNN regression. Xu et al. [52] and Lin et al. [31] adopted attention mechanisms to effectively integrate multi-modal features. Chen et al. [6] compared the performance of several regression models, among which XGBoost [7] exhibited the best results. Hsu et al. [22] employed LightGBM [23] and TabNet [2] to capture intricate semantic relationships in multi-modal features. Lai et al. [26] engineered handcrafted features, exploiting CatBoost for regression. Mao et al. [34] enhanced CatBoost-based model by stacking features. Tan et al. [44] extracted visual-textual features by ALBEF [29] and Chen et al. [8, 9] enriched more intermodal features to promote predictive performance. Wu et al. [50] emphasized increasing feature dimensions to improving predictive performance. The post dependencies captured by sliding window average [46] and DSN [54] has also led to improvements. Many of these multi-modal methods are based on the SMPD and working out great [49, 32].

Social media popularity datasets. Mazloom et al. [35] conducted experiments using a dataset of posts related to fast-food brands collected from Instagram. Sanjo et al. [42] provided a recipe popularity prediction dataset based on Cookpad, which includes text content entirely in Japanese. Li et al. [28] predicted the future popularity of topics by using historical sentiment information based on Twitter’s text data records. TPIC17 [47] and SMPD [48] are datasets for single popularity prediction task based on Flickr.

We believe that the loss of temporal alignment about popularity in existing methods is a common problem. The image dynamic popularity dataset [37] gave us insights, so we propose a multi-modal temporal popularity benchmark to address the shortcomings of existing studies.

3SMTPD Dataset
With the great development of web communication technologies, social multimedia has become the most popular media around the world. However, most existing social media prediction datasets are built on the basis of single-output prediction, meaning they observe existing posts and infer their popularity based on their posting time. As mentioned earlier, these data without aligned posting times exhibit non-uniform popularity distributions. Therefore, SMTPD keep an eye on one of the most popular worldwide social media, YouTube [5], with over 282K samples, primarily focusing on the evolution of popularity over time for these samples. We collected over 402K raw data samples. Specifically, we first removed records with missing values—which likely resulted from network issues during data acquisition. Next, we eliminated samples that either failed to be crawled on certain days or had been deleted within 30 days. Finally, we filtered out potential outliers using the 3
σ
 rule. In this section, we provide a comprehensive overview of the SMTPD’s composition. Additionally, we present various data analysis results that contribute to the feasibility of our approach.

Unlike the retrospective methods used in previous datasets, we take note of the newly posted multi-modal content and then observe popularity information every 24 hours via YouTube API. Considering that in real-world applications, the posts to be predicted are always new, this data observation method allows us to obtain aligned temporal popularity of new posts, which is more in line with practical applications.

Statistics	SMTPD	SMPD (Train/Test)
Number of samples	282.4K	305K/181K
Number of users	152.7K	38K/31K
Mean popularity	5.95	6.41/5.12
STD popularity	4.15	2.47/2.41
Number of categories	15	11
Number of custom tags	960K	250K
Average length of title	53.4 chars	29 words
Mean duration	1853.4 s	-
 
Table 2:The basic statistics of all samples in SMTPD, comparing to SMPD[48]. Due to the multilingual environment, we use chars (characters) to describe the average length of title.
Figure 1(a) show a sample from SMTPD. We note diverse attributes, including visual content, textual content, metadata, and user profiles. Additionally, we focus on the temporal popularity for each sample within 30 days after release. We perform basic statistics for SMTPD, as shown in Table 2.

3.1Temporal Popularity
The utilization of temporal popularity data is versatile. It not only serves as the output for predictions but also as inputs, where a segment preceding a specific time point, coupled with multi-modal content, can forecast subsequent popularity. We analyze the distribution and the correlation of popularity over time, so as to facilitate a comprehensive understanding of the significance of temporal popularity for predictions from different perspectives.

A number of popularity definitions have been born from previous work [27, 55]. We use Khosla’s popularity score transformation [24] as it can normalize the distribution of view counts to a suitable popularity score’s distribution. It can be represented as:

p
=
log
2
⁡
(
v
d
+
1
)
(1)
where 
p
 is the popularity score, 
v
 is the view counts of a sample, 
d
 represents the corresponding number of days after the post’s release. As shown in Figure 1, the histogram of view counts reveals an extreme long-tailed distribution, which might not be suitable as a prediction target. It’s evident that the distribution of the popularity score metric becomes more reasonable.

In addition, we notice that there is a strong correlation between the popularity scores of different days. The Pearson Correlation (PC) and Spearman Ranking Correlation (SRC) can respectively reflect the linear relationship and rank-order correlation between popularity scores of different days as follows:

P
⁢
C
=
∑
i
=
1
n
(
X
i
−
X
¯
)
⁢
(
Y
i
−
Y
¯
)
∑
i
=
1
n
(
X
i
−
X
¯
)
2
⁢
∑
i
=
1
n
(
Y
i
−
Y
¯
)
2
(2)
S
⁢
R
⁢
C
=
1
n
−
1
⁢
∑
i
=
1
n
(
X
i
−
X
¯
σ
X
)
⁢
(
Y
i
−
Y
¯
σ
Y
)
(3)
where 
X
 and 
Y
 denote the popularity scores belonging to 2 different days, while 
X
¯
 and 
σ
X
 denote the mean and standard deviation of 
X
, and similarly for 
Y
. PC and SRC respectively reflect the linear relationship and rank-order correlation between popularity scores of different days.

The Pearson Correlation (PC) and Spearman Rank Correlation (SRC) heat maps illustrate internal relationships in daily popularity scores, establishing a basis for prediction based on these temporal patterns. Further details are available in the supplementary materials.

3.2Multi-Modal Content
Multi-modal feature fusion is the mainstream approach in today’s popularity prediction methods. In this section, we will divide the data into corresponding modality and elucidate the multi-modal content in SMTPD.

3.2.1Visual Content
SMTPD samples, primarily drawn from a multi-modal social media platform, are heavily influenced by visual elements. Since metrics like view count and popularity score are often based on the cover frame that viewers see before clicking to play, we use the cover frame as the primary visual content. This approach balances popularity impact with copyright considerations.

3.2.2Textual Content
The textual content in posts plays a crucial role in media dissemination and user engagement. We examine several core elements, including category, title, description, and hashtags (denoted by the “#” symbol), along with the user ID (user nickname) from profile metadata. YouTube defines 15 distinct video categories, all in English, which support content organization and discovery. Figure 3 shows the statistical distribution of content by category.

Refer to caption
(c)The PC Matrix
Refer to caption
(d)The SRC Matrix
Figure 2:The heat map of daily popularity correlations. The figure clearly shows that there is a high degree of correlations in popularity between consecutive days.
As an international platform, YouTube hosts user-defined textual content in multiple languages beyond standard categories. Figure 4 illustrates the distribution and popularity bias across title languages.

In previous researches, the datasets typically had uniform language for text content, without considering multilingual aspects. While this simplifies modeling for prediction methods, it also poses significant limitations for international social media platforms which not restricted to a single language. Besides, predictions based on a few languages may introduce biases [16] against popularity.

3.2.3Numerical values
Numerical attributes frequently function as supplementary factors in enhancing prediction accuracy. In this study, we examined key attributes, including video duration, uploader follower count, and the number of posts by the uploader. Additionally, we manually derived several auxiliary metrics, such as title length, the count of custom tags, and description length, to further enrich the feature set and support predictive robustness.

4Temporal popularity prediction
The multi-modal feature-based temporal prediction framework is shown in Figure 5, which is divided into two main parts: multi-modal feature extraction and temporal popularity score regression. This framework is designed to adapt to the multilingual temporal prediction tasks under time alignment. The prediction target is set as the popularity of samples, which corresponds to the temporal popularity within 30 days after the sample’s release.

Refer to caption
(a)
Refer to caption
(b)
Figure 3:The statistics based on category. 3(a) counts the number of samples in each category, and 3(b) shows the average popularity score of samples in each category.
Refer to caption
Figure 4:Languages analysis. The left is the proportions of these languages, with ”Other” encompassing 90 different languages. The right represents the average popularity in different languages, revealing the geographic biases . The languages of samples are counted by reference to the title.
4.1Multi-Modal Feature Extraction
For different modalities in SMTPD, we adopted distinct feature extraction methods. We additionally incorporated features from the categorical modality to investigate the impact of categorical features on popularity prediction.

4.1.1Visual Features
The cover image of a social media content is a very important component which would help users to quickly understand what they would see if clicking to view this content. Therefore, the cover image would directly affect the popularity of a social media content. The semantic information provided in the cover image plays a key role for user’s understanding. We adopt convolutional neural networks ResNet-101 [20] pre-trained on ImageNet as our visual feature extraction model to obtain the semantic information provided by the cover. To match the input size of ResNet-101, we re-scale the size of cover image to 
224
×
224
. The 2048-dimension feature vector before the final classification layer will be selected as the final visual feature 
f
v
:

f
v
=
ResNet
⁢
(
𝒮
⁢
(
I
)
)
(4)
where 
I
 denotes the cover image and 
𝒮
 denotes the re-scale operation. However, the cover image would not always be uploaded by authors or be unavailable due to the network transmission. For those contents missing the cover image, we use blank images with all pixels are set to zero instead.

4.1.2Textual Features
Textual information significantly impacts a user’s choice to view or skip content. Key textual inputs include category, title, tags, description, and user profile ID. Extracting semantic features from these inputs is crucial for accurate popularity prediction.

However, unlike previous popularity prediction tasks, one distinguishing characteristic of SMTPD is that its text content includes multiple languages, and many samples contain text in more than one language. This makes it challenging to use many pre-trained word vector models based on single-language corpora, such as [18, 36, 38].

Thanks to the multilingual capability of BERT-Multilingual [12], which processes text across languages in a single model, we use it to extract a 768-dimensional feature vector for each text, capturing semantic information as:

f
t
k
=
BERT
⁢
(
T
k
)
(5)
Refer to caption
Figure 5:The proposed model consists of two layers. The upper layer processes visual, textual, numerical, and categorical features, which are input to a multi-layer perceptron (MLP). The MLP outputs are concatenated and fed into a lower LSTM layer for regression. Each LSTM cell’s output is passed through another MLP, with the final MLP outputs combined to generate a time prediction sequence using the ReLU activation function.
where 
k
∈
{
c
⁢
a
⁢
t
,
t
⁢
i
⁢
t
,
t
⁢
a
⁢
g
,
d
⁢
e
⁢
s
,
u
⁢
i
⁢
d
}
 maps to category, title, tags, description, and user ID. These are combined into a 
768
×
5
 matrix, transformed through 
5
×
5
 convolution to produce the 768D textual feature 
f
t
, which can be expressed as:

f
t
=
Conv
5
×
5
⁢
(
𝒞
⁢
(
f
t
c
⁢
a
⁢
t
,
f
t
t
⁢
i
⁢
t
,
f
t
t
⁢
a
⁢
g
,
f
t
d
⁢
e
⁢
s
,
f
t
u
⁢
i
⁢
d
)
)
(6)
where 
𝒞
 denotes the above combing operation.

4.1.3Numerical Features
Numerical metrics directly influence whether an audience clicks to watch which sample on social media platform. Also, the number of followers and the number of posts also impact the process through which an audience navigates from content uploaders’ user pages to click and watch videos. Hence, we selected these influential numerical metrics for numerical features extraction.As the number of user followers share a similar distribution pattern that exhibiting long-tailed characteristics as view counts, it is necessary to apply a logarithmic transformation before feeding it into the network. Afterward, all numerical items are Z-score normalized and concatenated as numerical features:

f
n
j
=
T
j
−
μ
j
σ
j
(7)
f
n
=
Concat
(
f
n
f
⁢
o
⁢
l
,
f
n
p
⁢
o
⁢
s
,
f
n
d
⁢
u
⁢
r
,
f
n
t
⁢
l
,
f
n
t
⁢
n
,
f
n
d
⁢
l
,
f
n
E
⁢
P
)
(8)
where 
j
∈
{
f
⁢
o
⁢
l
,
p
⁢
o
⁢
s
,
d
⁢
u
⁢
r
,
t
⁢
l
,
t
⁢
n
,
d
⁢
l
,
E
⁢
P
}
 represents the log-scaled follower counts, total number of posts, video duration, title length, the number of tags, description length and the early popularity (the 1st day’s popularity). The 
μ
 and 
σ
 represents the mean and standard deviation of all samples. And Concat denotes the horizontal concatenating operation.

4.1.4Categorical Features
The categorical disparities across social media platforms are depicted in Figure 3(b). Beyond text-based feature extraction, these disparities inform the generation of categorical features. Language functions as a key marker of regional and cultural distinctions among content creators, as highlighted by the language bias observed in Figure 4. Consequently, language classification features are crucial for enhancing prediction accuracy. To develop these classification features, two sub-features are selected: label and language attributes. The label feature captures the semantic category, while the language attribute is derived from the language in the video title. Assuming that the primary language of all text content matches the title’s language, we use langid [33] for classification. Two embedding layers are introduced to encode label and language features independently, each processed by a dedicated multi-layer perceptron (MLP). Finally, the outputs are combined via cumulative multiplication to form the classification feature 
f
c
, defined as:

f
c
=
MLP
1
⁢
(
E
1
⁢
(
T
c
⁢
a
⁢
t
)
)
⊙
MLP
2
⁢
(
E
2
⁢
(
langid
⁢
(
T
t
⁢
i
⁢
t
)
)
)
(9)
where 
E
1
 and 
E
2
 represent two independent embedding layers, and 
MLP
1
 and 
MLP
2
 refer to multi-layer perceptrons applied to the label embedding 
E
1
⁢
(
T
𝑐𝑎𝑡
)
 and the language embedding 
E
2
⁢
(
langid
⁢
(
T
𝑡𝑖𝑡
)
)
, respectively. The operator 
⊙
 denotes element-wise multiplication, which combines the outputs of the two MLPs to produce the final classification feature 
f
c
.

4.1.5Feature Fusion
After extraction, features from different modalities are aligned in dimension through multi-layer perceptrons (MLPs) and then concatenated into fused features 
F
.

4.2Temporal Popularity Regression
4.2.1Sequential Encoding and Adjustment
Considering the high correlation between popularity values on adjacent days in the ground truth, we employ a LSTM [21] structure to get the temporal variations in popularity. As shown in Figure 5, multiple LSTM cells are constructed to transmit temporal information. The initial states (both hidden state and cell state) of the LSTM are generated by passing the 
F
 through the same MLP as state encoding. Additionally, the input for LSTM cell at each time step is constructed from 
F
 through temporal encoding MLPs. These two encoding process can be written as:

h
0
=
c
0
=
MLP
hc
⁢
(
F
)
(10)
x
s
=
MLP
s
x
⁢
(
F
)
(11)
In this formulation, 
h
0
 and 
c
0
 denote the initial hidden state and cell state, while 
x
s
 represents the input at time step 
s
. The 
MLP
hc
 module encodes the state information, and 
MLP
s
x
 handles the temporal encoding at the 
s
-th time step, effectively capturing the sequence dynamics.

At each time step, both states are treated as the 
s
-th step’s features for output. After concatenating and processing through independent MLPs, each LSTM cell produces outputs, helping capture temporal popularity via backpropagation during training. Before final predictions, we apply a non-negative adjustment since popularity scores cannot be negative. This process is formulated as:

p
⁢
r
⁢
e
s
=
max
⁡
(
0
,
MLP
s
out
⁢
(
Concat
⁢
(
h
s
,
c
s
)
)
)
(12)
Where 
p
⁢
r
⁢
e
s
, 
h
s
, 
c
s
, and 
MLP
s
out
 denote the predicted value, hidden state, cell state, and output MLP at time step 
s
, respectively. The operation Concat refers to the process of horizontally concatenating the vectors. After these steps, the final temporal popularity predictions are produced.

4.2.2Loss Function
The core component of our approach is the Composite Gradient Loss (CGL), specifically designed for this task. This custom loss function consists of several components: SmoothL1Loss (SL) between the model’s outputs and targets, the first-order and second-order derivative differences between the outputs and targets, the L1 loss between the onehot encodings of the predicted and ground truth peaks, and the Laplacian remainder (LR). These components are combined with a weight ratio of 1:1:1:1e-6. The overall loss function 
ℒ
 is formulated as:

ℒ
=
SL
⁢
(
P
^
d
,
i
,
P
d
,
i
)
+
λ
1
⋅
SL
⁢
(
P
^
d
,
i
(
1
)
,
P
d
,
i
(
1
)
)
+
λ
2
⋅
SL
⁢
(
P
^
d
,
i
(
2
)
,
P
d
,
i
(
2
)
)
(13)
+
α
⋅
∑
i
=
1
n
|
δ
⁢
argmax
d
⁢
(
P
^
d
,
i
)
−
δ
⁢
argmax
d
⁢
(
P
d
,
i
)
|
+
ϵ
⋅
LR
And the Laplacian remainder is:

LR
=
∑
i
=
1
n
|
P
^
d
,
i
(
1
)
|
+
∑
i
=
1
n
|
P
^
d
,
i
(
2
)
|
(14)
The term 
SL
⁢
(
P
^
d
,
i
,
P
d
,
i
)
 (with 
β
=
0.1
) is used to compute the error between the predicted outputs and the ground truth targets. Here, 
P
^
d
,
i
 represents the predicted popularity for data point 
i
 on day 
d
, while 
P
d
,
i
 denotes the ground truth popularity for the same data point. The differences between the one-hot encoded predicted and true peak values are measured using 
δ
⁢
argmax
d
⁢
(
P
^
d
,
i
)
 and 
δ
⁢
argmax
d
⁢
(
P
d
,
i
)
, respectively. Additionally, the term 
ϵ
⋅
LR
 introduces a Laplacian remainder (LR) to provide further regularization. During training, the weights for the first-order and second-order derivative terms, as well as the L1 loss weight between the one-hot encodings (
λ
1
, 
λ
2
, 
α
), are adjusted dynamically using a cosine annealing algorithm to ensure smoother convergence throughout the training process.

5Experiments
In this section, we first describe the experiment settings and evaluation metrics for training models and comparison. Then various experimental results and detailed discussions are provided including evaluations for SMTPD dataset, proposed baseline, multi-modal features and early popularity.

5.1Experiment settings
We implement our approaches using the Pytorch* framework and train it with the Adam [25] optimizer incorporating L2 penalty of 
10
−
3
, while the batch size is set to 64. The learning rate is initialized to 
10
−
3
 and adjusted by the ReduceLROnPlateau scheduler provided by PyTorch when one epoch is end. Supervised training was performed using the Composite Gradient Loss (CGL) metioned before.

We introduce error-based metrics and correlation-based metrics to fairly evaluate the compared datasets and models. We introduce the Absolute Error (MAE) and average MAE (AMAE) to respectively evaluate models for single-day prediction and temporal prediction. Assuming that the daily MAE and average MAE are denoted as 
M
⁢
A
⁢
E
d
 and 
A
⁢
M
⁢
A
⁢
E
, they can be defined as:

M
⁢
A
⁢
E
d
=
1
n
⁢
∑
i
=
1
n
|
P
^
d
,
i
−
P
d
,
i
|
(15)
A
⁢
M
⁢
A
⁢
E
=
1
m
∑
d
=
1
m
M
⁢
A
⁢
E
d
(16)
where 
n
 denotes the total of samples and 
m
 denotes total of days, while the 
P
d
 and 
P
^
d
 respectively denotes the ground-truth popularity and predicted popularity for the day 
d
.

For correlation-based metrics, we introduce the daily SRC and the average SRC to evaluate the models for both single-day prediction and temporal prediction from a different perspective. Assuming 
n
, 
m
, 
P
d
, and 
P
^
d
 are defined consistently as mentioned earlier, the daily SRC and average SRC can be formulated as follows:

S
⁢
R
⁢
C
d
=
1
n
−
1
⁢
∑
i
=
1
n
(
P
^
d
,
i
−
P
^
¯
d
σ
P
^
d
)
⁢
(
P
d
,
i
−
P
¯
d
σ
P
d
)
(17)
A
⁢
S
⁢
R
⁢
C
=
1
m
⁢
∑
d
=
1
m
S
⁢
R
⁢
C
d
(18)
where 
P
d
¯
 and 
σ
P
d
 are mean and standard deviation of the corresponding popularity for the day 
d
.

In the curves, sequential performance is represented by the MAE and SRC metrics, which illustrate daily prediction errors and correlations for popularity scores. The X-axis denotes days, while the Y-axis shows 
M
⁢
A
⁢
E
d
 or 
S
⁢
R
⁢
C
d
.

5.2SMTPD VS. SMPD
In this subsection, we conduct comparisons and discussions between the SMTPD and SMPD. We first measure three most recently proposed state-of-the-art popularity prediction methods on two datasets. As these methods are all designed basing on the settings of SMPD, we make some modifications to let them fit for training and testing on our SMTPD. Other top-performing models (e.g. [46, 44, 50]) include components that are not applicable to SMTPD or are not reproducible, such as sliding window average or undisclosed self-trained modules. Hence, we do not discuss them in our experiments. First, we distribute content from corresponding modalities into their respective feature extraction modules. Then we use BERT-Multilingual as the textual feature extractor to address the challenges of multilingual text. Given that our SMTPD dataset consists of temporal popularity scores, we restrict these methods to predict only the single popularity score on day 30. To mitigate random bias, we evaluate using 
5
-fold cross-validation.

Table 4 shows minimal performance differences across folds, confirming that SMTPD contains abundant data under a well-balanced sample distribution. It is evident that on the single-output prediction of popularity on days 7, 14, and 30 within SMTPD, the performance of method [26] based on GBDT outperforms the deep learning method [13] and [52] in terms of both MAE and SRC through its powerful regression capabilities of Catboost [39]. Notably, our method achieves the best results with the addition of EP, where the AMAE of the other three models increases as the prediction horizon extends. In contrast, our model’s AMAE begins to decrease after day 14. The deep learning method [13] also performs well on days 7 and 14, but its effectiveness declines beyond day 14.

Morever there are also two interesting observation. First, all methods achieve higher SRC on SMTPD than on SMPD, likely because SMPD lacks specific time points, making it challenging to predict time-dependent popularity trends accurately as popularity declines and their MAE performances are certainly reduced that the MAE values increase by over 0.16. Besides, the larger popularity range and standard deviation among SMTPD samples (shown in Table 2) also contributes to prediction difficulties.

BERT-Base	BERT-Mul	MLP	LSTM	AMAE	ASRC
✓			✓	0.782	0.958
✓	✓		0.786	0.958
✓		✓	0.717	0.959
 
Table 3:The evaluation for the proposed baseline model, mainly on evaluating the model’s performance in adapting to multilingual and temporal popularity.
Method	SMTPD (day 7)	SMTPD (day 14)	SMTPD (day 30)
Average	Average	Average
Ding et al. [13] 	1.715/0.849	1.669/0.846	1.592/0.843
w. EP	0.715/0.964	0.742/0.959	0.749/0.931
Lai et al. [26] 	1.573/0.875	1.524/0.872	1.495/0.864
w. EP	0.725/0.957	0.753/0.962	0.760/0.957
Xu et al. [52] 	1.895/0.817	1.832/0.818	1.743/0.820
w. EP	0.754/0.962	0.798/0.956	0.822/0.949
Ours w/o. EP	1.673/0.852	1.628/0.850	1.563/0.848
Ours	0.713/0.964	0.735/0.959	0.732/0.959
 
Table 4:The performance (MAE/SRC) was compared across four models, including our model, using the SMTPD dataset, both with and without EP.
5.3Evaluation for Proposed Baseline
Refer to Table 3, we attempted to validate the rationale of partial structures in the proposed baseline model by employing alternative feature extractors and regression networks. Using BERT-Base as the textual features extractor lead to an increase of MAE by around 0.19. This decline in performance may be caused by the limitations of BERT-base model in handling multilingual texts, as it struggles to effectively capture the semantics and contextual information across different languages. The MAE also increased when the MLP (3 layers) was used as the regression structure. Such a structure is similar to [13], suggesting that MLP lacks the capture of temporal information. The SRC did not change for either of the above substitutions, probably due to the high correlation given by EP.

5.4Discussion of Early Popularity
We evaluate the performance of proposed baseline on SMTPD.As shown in Table 5, the proposed baseline gets a great improvement from existed methods that surpassing the second best method by -0.798/0.109 MAE/SRC for predicting the popularity of day 30. This great improvement is mainly brought by the early popularity (EP). Without the assistant of EP (row 2 in Table 5), the baseline performance sharply reduced around the existed methods.Using the EP predicted by existed method (1.717/0.864 MAE/SRC) as an input also contributes to the baseline’s performance (row 3 in Table 5).However the performance gap between the predicted EP and true EP remains large.

Instead of directly involving the EP in the model architecture, introducing EP in the training supervision is another suitable option.To validate the effectiveness of such operation, we train a baseline model for predicting the popularities from day 1 to 30. As it presented by the row 1 in Table 5, adding the 1st day’s popularity to the prediction sequence make a slight boost, what is in line with the LSTM’s ability to capture temporal dependencies in popularity sequences. Having more preceding temporal information from backpropagation leads to more precise predictions of popularity in subsequent time steps.

These comparisons clearly indicate that EP plays a crucial role in popularity prediction, and accurately forecasting the first day’s popularity is key to predicting future popularity. The strong correlation between EP and future popularity significantly benefits the prediction task. Our results, as demonstrated by the MAE and SRC curves for both natural EP and our model’s predictions, underscore the model’s capability to leverage EP for enhanced accuracy. From the visualized results, tough EP exhibits high correlation to the popularities of following days, the MAE sharply increased over time. By contrast, our baseline model could well optimize the MAE and achieve even better SRC performance comparing to the natural EP curve. Therefore, the proposed baseline model is effective to utilize EP achieving better prediction accuracy.

Method	AMAE	ASRC	MAE	SRC
(day 30 only)	(day 30 only)
w/o. EP(1-30)	1.562	0.856	1.530	0.850
w/o. EP(2-30)	1.630	0.849	1.551	0.849
w/o. EP+[26] 	1.628	0.851	1.555	0.848
ours	0.717	0.959	0.732	0.959
 
Table 5:Assessment of EP across different scenarios. Here, ”1-30” denotes the prediction target spanning a continuous sequence from the 1st day to the 30th day, as does ”2-30” (to align with methods having EP).
6Conclusion
This study aims to address the challenge of time-series popularity prediction in social media. In this paper, we introduce a novel multilingual, multi-modal time-series popularity dataset based on YouTube and suggest a multilingual temporal prediction model tailored to this dataset. Through experiments, we demonstrate the effectiveness of this approach in predicting social media popularity time-series in a multilingual environment. The experiments show that combining multi-modal features with early popularity significantly improves prediction accuracy. However, this study has yet to address challenges such as multi-frame information in videos, maximizing the use of language diversity, and deeper multi-modal exploration. These areas will be key focuses for our future work.

References
Agarwal et al. [2008]
Deepak Agarwal, Bee-Chung Chen, Pradheep Elango, Nitin Motgi, Seung-Taek Park, Raghu Ramakrishnan, Scott Roy, and Joe Zachariah.Online models for content optimization.Advances in Neural Information Processing Systems, 21, 2008.
Arik and Pfister [2021]
Sercan Ö Arik and Tomas Pfister.Tabnet: Attentive interpretable tabular learning.In Proceedings of the AAAI conference on artificial intelligence, pages 6679–6687, 2021.
Bao et al. [2013]
Peng Bao, Hua-Wei Shen, Junming Huang, and Xue-Qi Cheng.Popularity prediction in microblogging network: a case study on sina weibo.In Proceedings of the 22nd international conference on world wide web, pages 177–178, 2013.
Bao et al. [2007]
Shenghua Bao, Guirong Xue, Xiaoyuan Wu, Yong Yu, Ben Fei, and Zhong Su.Optimizing web search using social annotations.In Proceedings of the 16th international conference on World Wide Web, pages 501–510, 2007.
Ceci [2022]
Laura Ceci.Youtube-statistics & facts.Statista. com [online].[cit. 2022-05-05]. Dostupné z: https://www. statista. com/topics/2019/youtube, 2022.
Chen et al. [2019]
Junhong Chen, Dayong Liang, Zhanmo Zhu, Xiaojing Zhou, Zihan Ye, and Xiuyun Mo.Social media popularity prediction based on visual-textual features with xgboost.In Proceedings of the 27th ACM International Conference on Multimedia, pages 2692–2696, 2019.
Chen and Guestrin [2016]
Tianqi Chen and Carlos Guestrin.Xgboost: A scalable tree boosting system.In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining, pages 785–794, 2016.
Chen et al. [2022]
Weilong Chen, Chenghao Huang, Weimin Yuan, Xiaolu Chen, Wenhao Hu, Xinran Zhang, and Yanru Zhang.Title-and-tag contrastive vision-and-language transformer for social media popularity prediction.In Proceedings of the 30th ACM International Conference on Multimedia, pages 7008–7012, 2022.
Chen et al. [2023]
Xiaolu Chen, Weilong Chen, Chenghao Huang, Zhongjian Zhang, Lixin Duan, and Yanru Zhang.Double-fine-tuning multi-objective vision-and-language transformer for social media popularity prediction.In Proceedings of the 31st ACM International Conference on Multimedia, pages 9462–9466, 2023.
Cheng et al. [2021]
Wen-Huang Cheng, Sijie Song, Chieh-Yun Chen, Shintami Chusnul Hidayati, and Jiaying Liu.Fashion meets computer vision: A survey.ACM Computing Surveys (CSUR), 54(4):1–41, 2021.
Cho et al. [2024]
Minhwa Cho, Dahye Jeong, and Eunil Park.Amps: Predicting popularity of short-form videos using multi-modal attention mechanisms in social media marketing environments.Journal of Retailing and Consumer Services, 78:103778, 2024.
Devlin et al. [2019]
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.Bert: Pre-training of deep bidirectional transformers for language understanding.In Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, pages 4171–4186, 2019.
Ding et al. [2019]
Keyan Ding, Ronggang Wang, and Shiqi Wang.Social media popularity prediction: A multiple feature fusion approach with deep neural networks.In Proceedings of the 27th ACM International Conference on Multimedia, pages 2682–2686, 2019.
Gharibshah and Zhu [2021]
Zhabiz Gharibshah and Xingquan Zhu.User response prediction in online advertising.aCM Computing Surveys (CSUR), 54(3):1–43, 2021.
Ghose and Yang [2009]
Anindya Ghose and Sha Yang.An empirical analysis of search engine advertising: Sponsored search in electronic markets.Management science, 55(10):1605–1622, 2009.
Ghosh et al. [2021]
Sayan Ghosh, Dylan Baker, David Jurgens, and Vinodkumar Prabhakaran.Detecting cross-geographic biases in toxicity modeling on social media.In Proceedings of the Seventh Workshop on Noisy User-generated Text (W-NUT), pages 313–328, 2021.
Gonçalves et al. [2010]
Marcos André Gonçalves, Jussara M Almeida, Luiz GP dos Santos, Alberto HF Laender, and Virgilio Almeida.On popularity in the blogosphere.IEEE Internet Computing, 14(3):42–49, 2010.
Grave et al. [2018]
Edouard Grave, Piotr Bojanowski, Prakhar Gupta, Armand Joulin, and Tomas Mikolov.Learning word vectors for 157 languages.In Proceedings of the International Conference on Language Resources and Evaluation (LREC), 2018.
Hajarian et al. [2021]
Mohammad Hajarian, Mark Anthony Camilleri, Paloma Díaz, and Ignacio Aedo.A taxonomy of online marketing methods.In Strategic corporate communication in the digital age, pages 235–250. Emerald Publishing Limited, 2021.
He et al. [2016]
Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.Deep residual learning for image recognition.In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 770–778, 2016.
Hochreiter and Schmidhuber [1997]
Sepp Hochreiter and Jürgen Schmidhuber.Long short-term memory.Neural computation, 9(8):1735–1780, 1997.
Hsu et al. [2023]
Chih-Chung Hsu, Chia-Ming Lee, Xiu-Yu Hou, and Chi-Han Tsai.Gradient boost tree network based on extensive feature analysis for popularity prediction of social posts.In Proceedings of the 31st ACM International Conference on Multimedia, pages 9451–9455, 2023.
Ke et al. [2017]
Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, and Tie-Yan Liu.Lightgbm: A highly efficient gradient boosting decision tree.Advances in neural information processing systems, 30, 2017.
Khosla et al. [2014]
Aditya Khosla, Atish Das Sarma, and Raffay Hamid.What makes an image popular?In Proceedings of the 23rd international conference on World wide web, pages 867–876, 2014.
Kingma and Ba [2015]
Diederik P Kingma and Jimmy Ba.Adam: A method for stochastic optimization.In Proceedings of the 3rd International Conference on Learning Representations(ICLR),San Diego,California,USA,May 7-9, 2015.
Lai et al. [2020]
Xin Lai, Yihong Zhang, and Wei Zhang.Hyfea: Winning solution to social media popularity prediction for multimedia grand challenge 2020.In Proceedings of the 28th ACM International Conference on Multimedia, pages 4565–4569, 2020.
Li et al. [2016]
Chenyu Li, Jun Liu, and Shuxin Ouyang.Analysis and prediction of content popularity for online video service: a youku case study.China Communications, 13(12):216–233, 2016.
Li et al. [2019]
Jinning Li, Yirui Gao, Xiaofeng Gao, Yan Shi, and Guihai Chen.Senti2pop: sentiment-aware topic popularity prediction on social media.In 2019 IEEE International conference on data mining (ICDM), pages 1174–1179. IEEE, 2019.
Li et al. [2021]
Junnan Li, Ramprasaath Selvaraju, Akhilesh Gotmare, Shafiq Joty, Caiming Xiong, and Steven Chu Hong Hoi.Align before fuse: Vision and language representation learning with momentum distillation.Advances in neural information processing systems, 34:9694–9705, 2021.
Lifshits [2010]
Yury Lifshits.Ediscope: Social analytics for online news.Yahoo Labs, 2010.
Lin et al. [2022]
Hung-Hsiang Lin, Jiun-Da Lin, Jose Jaena Mari Ople, Jun-Cheng Chen, and Kai-Lung Hua.Social media popularity prediction based on multi-modal self-attention mechanisms.IEEE Access, 10:4448–4455, 2022.
Liu et al. [2022]
An-An Liu, Xiaowen Wang, Ning Xu, Junbo Guo, Guoqing Jin, Quan Zhang, Yejun Tang, and Shenyuan Zhang.A review of feature fusion-based media popularity prediction methods.Visual Informatics, 2022.
Lui and Baldwin [2012]
Marco Lui and Timothy Baldwin.langid.py: An off-the-shelf language identification tool.In Proceedings of the ACL 2012 System Demonstrations, pages 25–30, 2012.
Mao et al. [2023]
Shijian Mao, Wudong Xi, Lei Yu, Gaotian Lü, Xingxing Xing, Xingchen Zhou, and Wei Wan.Enhanced catboost with stacking features for social media prediction.In Proceedings of the 31st ACM International Conference on Multimedia, pages 9430–9435, 2023.
Mazloom et al. [2016]
Masoud Mazloom, Robert Rietveld, Stevan Rudinac, Marcel Worring, and Willemijn Van Dolen.Multimodal popularity prediction of brand-related social media posts.In Proceedings of the 24th ACM international conference on Multimedia, pages 197–201, 2016.
Mikolov et al. [2013]
Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean.Efficient estimation of word representations in vector space.In Proceedings of the 1st International Conference on Learning Representations(ICLR),Scottsdale,Arizona,USA,May 2-4, 2013.
Ortis et al. [2019]
Alessandro Ortis, Giovanni Maria Farinella, and Sebastiano Battiato.Prediction of social image popularity dynamics.In Image Analysis and Processing–ICIAP 2019: 20th International Conference, Trento, Italy, September 9–13, 2019, Proceedings, Part II 20, pages 572–582. Springer, 2019.
Pennington et al. [2014]
Jeffrey Pennington, Richard Socher, and Christopher D Manning.Glove: Global vectors for word representation.In Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP), pages 1532–1543, 2014.
Prokhorenkova et al. [2018]
Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush, and Andrey Gulin.Catboost: unbiased boosting with categorical features.Advances in neural information processing systems, 31, 2018.
Richier et al. [2014a]
Cédric Richier, Eitan Altman, Rachid Elazouzi, Tania Altman, Georges Linares, and Yonathan Portilla.Modelling view-count dynamics in youtube.CoRR, abs/1404.2570, 2014a.
Richier et al. [2014b]
Cedric Richier, Eitan Altman, Rachid Elazouzi, Tania Jimenez, Georges Linares, and Yonathan Portilla.Bio-inspired models for characterizing youtube viewcout.In 2014 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM), pages 297–305. IEEE, 2014b.
Sanjo and Katsurai [2017]
Satoshi Sanjo and Marie Katsurai.Recipe popularity prediction with deep visual-semantic fusion.In Proceedings of the 2017 ACM on Conference on Information and Knowledge Management, pages 2279–2282, 2017.
Szabo and Huberman [2010]
Gabor Szabo and Bernardo A Huberman.Predicting the popularity of online content.Communications of the ACM, 53(8):80–88, 2010.
Tan et al. [2022]
YunPeng Tan, Fangyu Liu, BoWei Li, Zheng Zhang, and Bo Zhang.An efficient multi-view multimodal data processing framework for social media popularity prediction.In Proceedings of the 30th ACM International Conference on Multimedia, pages 7200–7204, 2022.
Tatar et al. [2014]
Alexandru Tatar, Marcelo Dias De Amorim, Serge Fdida, and Panayotis Antoniadis.A survey on predicting the popularity of web content.Journal of Internet Services and Applications, 5(1):1–20, 2014.
Wang et al. [2020]
Kai Wang, Penghui Wang, Xin Chen, Qiushi Huang, Zhendong Mao, and Yongdong Zhang.A feature generalization framework for social media popularity prediction.In Proceedings of the 28th ACM International Conference on Multimedia, pages 4570–4574, 2020.
Wu et al. [2017]
Bo Wu, Wen-Huang Cheng, Yongdong Zhang, Qiushi Huang, Jintao Li, and Tao Mei.Sequential prediction of social media popularity with deep temporal context networks.In Proceedings of the 26th International Joint Conference on Artificial Intelligence (IJCAI), pages 3062–3068, 2017.
Wu et al. [2019]
Bo Wu, Wen-Huang Cheng, Peiye Liu, Bei Liu, Zhaoyang Zeng, and Jiebo Luo.Smp challenge: An overview of social media prediction challenge 2019.In Proceedings of the 27th ACM International Conference on Multimedia, pages 2667–2671. ACM, 2019.
Wu et al. [2023a]
Bo Wu, Peiye Liu, Wen-Huang Cheng, Bei Liu, Zhaoyang Zeng, Jia Wang, Qiushi Huang, and Jiebo Luo.Smp challenge: An overview and analysis of social media prediction challenge.In Proceedings of the 31st ACM International Conference on Multimedia, pages 9651–9655, 2023a.
Wu et al. [2022]
Jianmin Wu, Liming Zhao, Dangwei Li, Chen-Wei Xie, Siyang Sun, and Yun Zheng.Deeply exploit visual and language information for social media popularity prediction.In Proceedings of the 30th ACM International Conference on Multimedia, pages 7045–7049, 2022.
Wu et al. [2023b]
Leilei Wu, Lingling Yi, Xiao-Long Ren, and Linyuan Lü.Predicting the popularity of information on social platforms without underlying network structure.Entropy, 25(6):916, 2023b.
Xu et al. [2020]
Kele Xu, Zhimin Lin, Jianqiao Zhao, Peicang Shi, Wei Deng, and Huaimin Wang.Multimodal deep learning for social media popularity prediction with attention mechanism.In Proceedings of the 28th ACM International Conference on Multimedia, pages 4580–4584, 2020.
Yang and Leskovec [2011]
Jaewon Yang and Jure Leskovec.Patterns of temporal variation in online media.In Proceedings of the fourth ACM international conference on Web search and data mining, pages 177–186, 2011.
Zhang et al. [2023]
Zhizhen Zhang, Xiaohui Xie, Mengyu Yang, Ye Tian, Yong Jiang, and Yong Cui.Improving social media popularity prediction with multiple post dependencies.CoRR, abs/2307.15413, 2023.
Zohourian et al. [2018]
Alireza Zohourian, Hedieh Sajedi, and Arefeh Yavary.Popularity prediction of images and videos on instagram.In 2018 4th International Conference on Web Research (ICWR), pages 111–117, 2018.