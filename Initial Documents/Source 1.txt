https://www.sciencedirect.com/science/article/abs/pii/S0969698924000742

Highlights
•
We provide a comprehensive dataset from YouTube Shorts for analysis of short-form video content.
•
We propose a novel CDF-based popularity standard, adaptable for real-world scenarios.
•
Implementing a multimodal attention mechanism to accurately predict the popularity of short-form videos.
•
We utilize the entire video frame, intra-modal and inter-modal relationships for the prediction.
Abstract
Emerging as a dominant content format amid the shift from television to mobile, short-form videos wield immense potential across diverse domains. However, the scarcity of datasets and established metrics for their popularity evaluation poses a challenge in accurately reflecting their real-world distribution. In response, our work introduces a dataset and pioneers a cumulative distribution function-based standard tailored specifically for short-form videos. Our model, AMPS (Attention-based Multi-modal Popularity prediction model of Short-form videos) is designed to effectively forecast the popularity of these videos. Considering YouTube Shorts, typically confined to under one minute, our research capitalizes on complete video frames for a holistic prediction of popularity. AMPS harnesses BiLSTM with Self-Attention and Co-Attention mechanisms, enabling a deeper understanding of intra-modal and inter-modal relationships across various modalities. Leveraging full video frame representation, our model significantly enhances prediction accuracy. Comprehensive evaluations against baseline models and machine learning algorithms consistently showcase AMPS' superiority in metrics like G-Mean, average F1-score, and Accuracy. Furthermore, when compared with other open social media datasets, our dataset coupled with AMPS consistently outperforms, affirming its robustness and reliability. Additionally, ablation studies underscore the effectiveness of AMPS' architecture and highlight the significance of each modality in predicting popularity.
Introduction
As the shift in content consumption moved from TV to mobile devices, vertical short-form videos have emerged (Canella, 2018). These videos, lasting less than one minute, are designed for easy viewing on mobile devices, offering convenience and accessibility anytime, anywhere. According to a 2020 Hootsuite research (Digital 2020, 2023), there are 480 million mobile internet users, representing a significant portion of the global population. Furthermore, the consumption of mobile videos continues to show remarkable growth, doubling each year. These statistics suggest a forthcoming increase in mobile platforms offering short-form video content (Canella, 2018; Okazaki and Barwise, 2011). Aligned with these trends, social media and video platforms, including Instagram, YouTube, and Netflix, have introduced short-form video platforms such as Reels, Shorts, and Fast Laughs. In addition, platforms specializing in short-form content such as TikTok have gained popularity in the global video content market (Chandrasekaran et al., 2019).
Short-form videos have found application across diverse fields and presented considerable market scalability (Dolega et al., 2021; Agrawal and Mittal, 2022). Their exceptional accessibility, allowing users to consume content anytime, anywhere via mobile devices, facilitates their versatile use across various domains (Mondal et al., 2023). In particular, these videos have gained significant popularity due to their convenience during commutes or short breaks. Furthermore, their ease of creation has led to a wide array of content (Zhou, 2019). Capitalizing on these advantages, short-form videos have transcended mere entertainment and expanded into realms such as marketing, advertising, news production, and education. They have become a potent tool for conveying varied messages and disseminating information succinctly (Song et al., 2021; Assad, 2023; Zhang, 2020; Nguyen and Diederich, 2023).
According to statistics from Collab Asia, a company specializing in YouTube creators, channels incorporating Shorts experience a 2.3-fold increase in average watch time compared to those that do not (Contents Korea 2023, 2023). This underscores the surging popularity of short-form content and aligns with YouTubes' decision to diversify ad revenue distribution, earmarking a share for short-form creators starting in February 2023 (Youtube Shorts monetization policies, 2023). This dynamic shift is expected to foster the emergence of more creators and the expansion of diverse businesses. Hence, understanding and predicting the trajectory of short-form content popularity is crucial in this evolving media landscape.
While various studies have delved into predicting content popularity (Arora et al., 2019; Ladhari et al., 2020), there is a notable dearth of research and datasets specifically dedicated to forecasting the popularity of short-form videos. Among the existing studies addressing this objective, one utilized Graph Convolutional Networks (GCN) to forecast the popularity of short videos (Zhang et al., 2020). However, their approach primarily centered on community-based analysis and lacked detailed examination of the specific elements within short-form videos that influence their popularity. Consequently, we curated a dataset integrating metadata sourced from YouTube Shorts, laying the groundwork for more comprehensive exploration in this domain. The dataset is available at https://github.com/dxlabskku/AMPS_short-form-popularity.
In the majority of previous studies, a popularity score, referenced in works such as (Khosla et al., 2014; Zohourian et al., 2018; Said et al., 2020; Bielski and Trzcinski, 2018), was established to forecast popularity. This metric served as a benchmark for the regression or categorization of popular videos. However, the popularity standards set in these earlier studies pose challenges in mirroring the distribution of popular videos in the real world, as they normalized the popularity score using equal proportions or the median. Consequently, we propose an alternative popularity standard specifically tailored to suit short-form videos, aiming to complement and augment the existing popularity score.
A number of scholars have overlooked both intra-modal interactions and inter-modal relationships in popularity prediction. Understanding intra-model interactions allows for the identification of influential information within each modality, while leveraging inter-model interactions harnesses the complementary strengths between modalities. These interactions play notable roles in acquiring high-level contextual information through multi-modalities (Sun et al., 2021)
Hence, we introduce the Attention-based Multi-modal Popularity Prediction of Short-form videos Model (AMPS). AMPS utilizes an Attention Mechanism to comprehend high-level contextual information across multiple modalities for predicting popularity. By employing BiLSTM and Self-Attention Mechanism, it adeptly captures essential information and patterns within sequential video and text modalities (S. et al., 2022; Qiu et al., 2022; Xie et al., 2019). Moreover, the Co-Attention Mechanism facilitates understanding interactions between these modalities (Zou et al., 2022; Ghosal et al., 2018; Wu et al., 2021). In addition, AMPS, specifically targeting YouTube Shorts, aims to harness complete video frames for comprehensive popularity prediction.
We present a multimodal-based approach tailored for predicting the popularity of short-form videos. This paper delves into the following research questions (RQs):
•
RQ1: Can our popularity standard based on cumulative distribution function (CDF) be adaptable and effective in real-world scenarios?
•
RQ2: How do intra-modal and inter-modal relationships influence the effectiveness of popularity prediction models?
•
RQ3: What impact does utilizing the entire video frame have on predicting the popularity of short-form videos?
To assess the efficiency of the CDF-based popularity standard and our proposed Attention-based Multi-modal Popularity Prediction Model of Short-form videos Model (AMPS), we conducted experiments on the two datasets, comparing their performance against other models. Our findings demonstrate superior performance compared to the latest methods. In addition, we conducted ablation studies to validate the design choices made in the model. The main contributions of our research are as follows:
•
By constructing and providing a dataset from YouTube Shorts, a prominent platform for short-form videos, we offer a valuable resource for comprehending content within this format.
•
The introduction of our new popularity standard presents a more realistic and pragmatic approach to gauging content popularity, reflecting a shift towards a more practical measurement.
•
Our utilization of multi-modal information—video, text, and metadata features—through the implementation of an Attention mechanism provides methodological insights into the intricate relationships within and between modalities that influence popularity.
The structure of this paper is presented as follows: Section 2 initiates a comprehensive review of related work. Section 3 introduces the YouTube Shorts dataset we constructed and presents the proposed CDF-based popularity standard. Section 4 outlines the Attention-based Multi-modal Popularity Prediction Model of Short-form videos Model (AMPS). Sections 5 and 6 show our experiments with detailed results, and concluding remarks, respectively.
Access through your organization
Check access to the full text by signing in through your organization.

Section snippets
Uni-modal contents popularity prediction
Prior research focused on predicting content popularity primarily centered on images or videos (Liu et al., 2017). For instance, Ding et al. (2019) introduced a model for Automatic Image Popularity Assessment (IPA). This model integrates both visual and non-visual factors, employing a deep neural network to forecast the number of likes and comments an image might receive. Their experimentation on platforms such as Instagram and other social media platforms showcased exceptional performance.
In
Data and popularity standard
Considering the absence of publicly available datasets tailored for short-form videos, we employed the YouTube Data API to curate our dataset. This dataset encompasses comprehensive details regarding both the video content itself and the associated channel information. Our methodology for data collection is extensively elucidated in Section 3.2, offering a meticulous breakdown of our approach.
Furthermore, to assess and quantify popularity within this dataset, we proposed a novel popularity
Method
We present our approach to feature extraction, specifically designed to effectively process various types of information from different modalities for predicting the popularity of YouTube Shorts. Furthermore, we detail the construction of a multi-modal model leveraging these extracted features. The comprehensive structure of the proposed model, along with its architectural design, is visually presented in Fig. 3.
Experiments and results
In this section, we examine our experiments and their outcomes. First, we provide the details of our experiments, including the evaluation metrics employed to gauge our model performance, particularly in handling imbalanced classifications. We introduce the baseline models and additional datasets incorporated for comparison. In the results segment, we compare our model's performance against baseline models and other datasets. Furthermore, we present the findings of an ablation study,
Discussion and concluding remarks
The significance of short-form videos across diverse industries and their market scalability underscores the importance of research in predicting their popularity. However, several recent research encountered notable challenges attributed to various factors. First, there exists a scarcity of short-form video datasets within social media content. Second, a misalignment persists between prevailing popularity criteria and actual real-world scenarios.
Our paper introduces three pivotal contributions 
CRediT authorship contribution statement
Minhwa Cho: Writing – original draft, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. Dahye Jeong: Writing – review & editing, Validation, Software, Resources, Project administration. Eunil Park: Writing – review & editing, Validation, Supervision, Software, Funding acquisition.
Declaration of Competing Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
Acknowledgements
This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government (MSIT) (No. RS-2023-00254129, Graduate School of Metaverse Convergence (Sungkyunkwan University), and No. IITP-2024-2020-0-01816, ICAN Program).
References (71)
S.R. Agrawal et al.
Optimizing customer engagement content strategy in retail and e-tail: available on online product review videos
J. Retail. Consum. Serv.
(2022)
A. Arora et al.
Measuring social media influencer index-insights from Facebook, Twitter and Instagram
J. Retail. Consum. Serv.
(2019)
S. Chandrasekaran et al.
Evaluating marketer generated content popularity on brand fan pages–a multilevel modelling approach
Telemat. Inform.
(2019)
L.B. de Amorim et al.
The choice of scaling technique matters for classification performance
Appl. Soft Comput.
(2023)
L. Dolega et al.
Going digital? The impact of social media marketing on retail website traffic, orders and sales
J. Retail. Consum. Serv.
(2021)
K. Gedamu et al.
Relation-mining self-attention network for skeleton-based human action recognition
Pattern Recognit.
(2023)
H. Ji et al.
Fused deep neural networks for sustainable and computational management of heat-transfer pipeline diagnosis
Dev. Built Environ.
(2023)
J. Kim et al.
Predicting continuity of online conversations on reddit
Telemat. Inform.
(2023)
R. Ladhari et al.
Youtube vloggers' popularity and influence: the roles of homophily, emotional attachment, and expertise
J. Retail. Consum. Serv.
(2020)
T. Liu et al.
Interdisciplinary study on popularity prediction of social classified hot online events in China
Telemat. Inform.
(2017)