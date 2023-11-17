## Fake News Classifier 

Classifier employed to distinguish real from fake information. Applied it to identify major misinformation spreaders among highly followed accounts, addressing the issue of misinformation on social media.

● Leveraged Natural Language Processing (NLP) and Bidirectional Encoder Representations from Transformers (BERT) for tweet classification.

● Constructed a network graph illustrating connections among project-relevant accounts on Python and modeled the spread of misinformation across the network. Identified 40 potential spreader accounts out of the 70 under investigation.

● Implemented a BERT model for tweet classification utilizing a GPU accelerating the training of a 10.000 rows dataset, achieving 91% accuracy.

● Proposed and implemented the UIF metric for analyzing user impact on the spread of fake news on Twitter. This metric comes from a combination of user activity, follower count, and retweet potential, demonstrating its effectiveness in identifying fake news spreaders.

● Developed a BERT classifier to output a reputation score for each one of the users in the graph based on how much people generally agree with their opinions and information posted on social media.

● Executed ETL (Extract, Transform, Load) processes to streamline data obtained from the Twitter API into structured databases. Increased the lab’s data processing capabilities by 46%, enhancing efficiency in handling large datasets and facilitating more effective analysis.

## Classifier confusion matrix

![image](https://github.com/jzuluaga02/data-science-portfolio/assets/114960212/84d612b9-668f-45e0-9410-a28d16f7fbbd)

## UIF Score vs Original probability

![image](https://github.com/jzuluaga02/data-science-portfolio/assets/114960212/65f10998-861e-40e8-852e-1d1e90fe507a)

