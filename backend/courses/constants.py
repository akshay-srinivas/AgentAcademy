COURSES = [
    {
        "title": "LLM University",
    }
]


MODULES = [
    {
        "course_title": "LLM University",
        "modules" : [
            {
                "title" : "Large Language Models",                
            },
            {
                "title" : "Text Representation",
            },
            {
                "title" : "Text Generation",
            },
            {
                "title" : "Deployment",
            },
            {
                "title" : "Semantic Search",
            },
            {
                "title" : "Prompt Engineering",
            },
            {
                "title" : "Retrieval-Augmented Generation (RAG)",
            },
            {
                "title" : "Tool Use",
            },
            {
                "title" : "Cohere on AWS",
            }
        ]
    }
]

LESSONS = [
    {
        "module_title" : "Large Language Models",
        "lessons" : [
            {
                "title" : "What Are Word and Sentence Embeddings?",
                "content_type" : "text",
                "estimated_duration" : 10,
                "is_mandatory" : True,
            },
            {
                "title" : "What is Similarity Between Sentences?",
                "content_type" : "text",
                "estimated_duration" : 10,
                "is_mandatory" : True,
            },
            {
                "title" : "What Is Attention in Language Models?",
                "content_type" : "text",
                "estimated_duration" : 10,
                "is_mandatory" : True,
            },
            {
                "title" : "What Are Transformer Models and How Do They Work?",
                "content_type" : "text",
                "estimated_duration" : 10,
                "is_mandatory" : True,
            }
        ]
    },
    {
        "module_title" : "Text Representation",
        "lessons" : [
            {
                "title" : "Introduction to Text Embeddings",
                "content_type" : "text",
                "estimated_duration" : 10,
                "is_mandatory" : True,
            }
        ]
    },
    {
        "module_title" : "Text Generation",
        "lessons" : [
            {
                "title" : "Introduction to Text Generation",
                "content_type" : "text",
                "estimated_duration" : 10,
                "is_mandatory" : True,
            }
        ]
    }
]


LESSON_CONTENT = [
    {
        "lesson_title" : "What Are Word and Sentence Embeddings?",
        "text_content" : """
Sentence and word embeddings are the bread and butter of language models. Here is a very simple introduction to what they are.

Word and sentence embeddings are the bread and butter of language models. This chapter shows a very simple introduction to what they are.

In old futuristic movies, such as the 2001 Space Odyssey, the main computer (HAL) was able to talk to humans and understand what they would say with great ease. At the time, getting computers to understand and produce language seemed like an impossible task, but the latest large language models (LLM) are able to do this in a way that makes it almost impossible for a human to tell if they are talking to another human, or to a computer.

The quintessential task of natural language processing (NLP) is to understand human language. However, there is a big disconnection there. Humans speak in words and sentences, but computers only understand and process numbers. How can we turn words and sentences into numbers in a coherent way? An assignment of words to numbers is called a word embedding. We can think of a word embedding as an assignment of scores to the words, with some nice properties (that we’ll learn soon).

# What is a Word Embedding?
Before we get into what is a word embedding, let me test your intuition. In the figure underneath (Quiz 1), I have located 12 words in the plane. The words are the following:

- Banana
- Basketball
- Bicycle
- Building
- Car
- Castle
- Cherry
- House
- Soccer
- Strawberry
- Tennis
- Truck

Now, the question is, where would you locate the word “Apple” in this plane? There are many places it could go, but I’m allowing 3 possibilities labeled A, B, and C.

![quiz1](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fembeddings-quiz-1.png&w=3840&q=75)

What I would do, is locate it in point C, because it would make sense to have the word “Apple” close to the words “Banana”, “Strawberry”, and “Cherry”, and far from the other words such as “House”, “Car”, or “Tennis”. This is precisely a word embedding. And what are the numbers we are assigning to each word? Simply the horizontal and vertical coordinates of the location of the word. In this way, the word “Apple” is assigned to the numbers [5,5], and the word “Bicycle” to the coordinates [5,1].

For the sake of redundancy, let’s enumerate some properties that a nice word embedding should have:

- Words that are similar should correspond to points that are close by (or equivalently, to scores that are similar).
- Words that are different should correspond to points that are far away (or equivalently, to scores that are significantly different).

# Word Embeddings Capture Features of the Word

The word embedding above satisfies properties 1 and 2. Is that it? Not yet. There is something more to these word embeddings, and it is that they don’t only capture word similarity, but they also capture other properties of the language. In language, words can be combined to get more complicated concepts. In mathematics, numbers can be added or subtracted to get other numbers. Could we build a word embedding that captures relations between words, as relations between numbers?

Let’s look at four words, “Puppy”, “Dog”, “Calf”, and “Cow”. These words are clearly correlated. Now to test your intuition again, I’m going to locate the words “Puppy”, “Dog”, and “Calf” in the plane, and I’ll ask you to add the word “Cow”. Where would you add it, in the spot labeled A, B, or C?

![quiz2](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fembeddings-quiz-2.png&w=3840&q=75)

While it would make sense to locate it in A, closer to “Calf” since they are both bovine, or in B, since it’s an adult animal, like “Dog”, the place where I would put this is in spot C, with coordinates [3,4]. Why? Because the rectangle formed by the four words captures some very important relationships between them. For instance, two analogies are captured here. The analogy “A puppy is to a dog like a calf is to a cow” can be translated into “The path from the word puppy to the word dog is the same as the path from the word calf to the word cow”. The analogy “A dog is to a cow like a puppy is to a calf” is also captured in this rectangle, as it’s shown in the figure below.

However, this is not even the tip of the iceberg. The main property of word embeddings that is in effect here is that the two axes (vertical and horizontal) represent different things. If you look carefully, moving towards the right turns the puppy into a dog, and the calf into a cow, which is an increase in age. Likewise, moving upwards turns a puppy into a calf and a dog into a cow, which is an increase in the size of the animal. It seems that this embedding is understanding that the words in it have two main properties, or features: age and size. Furthermore, it seems that the embedding is locating age in the horizontal axis and size in the vertical axis. In that case, where would you imagine that the word “whale” goes? Probably somewhere above the word “cow”. And if there was a word for “really old dog”? That word would go somewhere to the right of the word “dog”.

A good word embedding would be able to capture not only age and size, but also many more features of the words. Since each feature is one new axis, or coordinate, then a good embedding must have many more than two coordinates assigned to every word. One of the Cohere embeddings, for example, has 1024 coordinates associated with each word. These rows of 1024 (or however many) coordinates are called vectors, so we often talk about the vector corresponding to a word, and to each of the numbers inside a vector as a coordinate. Some of these coordinates may represent important properties of the word, such as age, gender, size. Some may represent combinations of properties. But some others may represent obscure properties that a human may not be able to understand. But all in all, a word embedding can be seen as a good way to translate human language (words) into computer language (numbers), so that we can start training machine learning models with these numbers.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fword-embeddings.png&w=3840&q=75)

# Sentence Embeddings
So word embeddings seem to be pretty useful, but in reality, human language is much more complicated than simply a bunch of words put together. Human language has structure, sentences, etc. How would one be able to represent, for instance, a sentence? Well, here’s an idea. How about the sums of scores of all the words? For example, say we have a word embedding that assigns the following scores to these words:
No: [1,0,0,0]
I: [0,2,0,0]
Am: [-1,0,1,0]
Good: [0,0,1,3]
Then the sentence “No, I am good!” corresponds to the vector [0,2,2,3]. However, the sentence “I am no good” will also correspond to the vector [0,2,2,3]. This is not a good thing, since the computer understand these two sentences in the exact same way, yet they are quite different, almost opposite sentences! Therefore, we need better embeddings that take into account the order of the words, the semantics of the language, and the actual meaning of the sentence.

This is where sentence embeddings come into play. A sentence embedding is just like a word embedding, except it associates every sentence with a vector full of numbers, in a coherent way. By coherent, I mean that it satisfies similar properties as a word embedding. For instance, similar sentences are assigned to similar vectors, different sentences are assigned to different vectors, and most importantly, each of the coordinates of the vector identifies some (whether clear or obscure) property of the sentence.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fsentence-embeddings.png&w=3840&q=75)

The Cohere embedding does just this. Using transformers, attention mechanisms, and other cutting edge algorithms, this embedding sends every sentence to a vector formed by 4096 numbers, and this embedding works really well. As a small example, here is a heatmap of an embedding containing 10 entries for each sentence, for several sentences (writing the entire 4096 entries will take too much space, so we compressed it using a dimensionality reduction algorithm called Principal Component Analysis.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fvisualizing-embeddings.png&w=3840&q=75)

Notice that these sentences are all very similar. In particular, the three highlighted sentences pretty much have the same meaning. If you look at their corresponding vectors, these are also really similar. That is exactly what an embedding should do.

# How to Use These Embeddings?
Now that you’ve learned how useful these embeddings are, it’s time to start playing with them and finding good practical uses for them! The Cohere dashboard provides a very friendly interface to use them. Here is a small example, with the following phrases:

I like my dog
I love my dog
I adore my dog
Hello, how are you?
Hey, how's it going?
Hi, what's up?
I love watching soccer
I enjoyed watching the world cup
I like watching soccer matches

To see the results of the sentence embedding, go to the “Embed” tab in the Cohere dashboard, and type the sentences (click here for an embed demo you can play with).

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F18ecd8a-image.png&w=3840&q=75)

The results come out as vectors with 4096 entries for each sentence. These are obviously hard to visualize, but there is a way to bring them down to 2 entries per sentence in order to be easily visualized. This visualization is shown in the plot below.

https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fembeddings-2d.png&w=3840&q=75

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fembeddings-2d.png&w=3840&q=75)

Notice that the embedding seemed to capture the essence of the sentences, and there are 3 clear clusters of sentences. In the top left corner you find the sentences that greet a person, in the middle, those that talk about a person’s dog, and in the bottom right corner, those that talk about soccer. Notice that sentences such as “Hey what’s up” and “Hello, how are you?” have no words in common, yet the model can tell that they have the same meaning.

# Multilingual Sentence Embeddings
Most word and sentence embeddings are dependent on the language that the model is trained on. If you were to try to fit the French sentence “Bonjour, comment ça va?” (meaning: hello, how are you?) in the embedding from the previous section, it will struggle to understand that it should be close to the sentence “Hello, how are you?” in English. For the purpose of unifying many languages into one, and being able to understand text in all these languages, Cohere has trained a large multilingual model, that has showed wonderful results with more than 100 languages. Here is a small example, with the following sentences in English, French, and Spanish.

The bear lives in the woods
El oso vive en el bosque
L’ours vit dans la foret
The world cup is in Qatar
El mundial es en Qatar
La coupe du monde est au Qatar
An apple is a fruit
Una manzana es una fruta
Une pomme est un fruit
El cielo es azul
The sky is blue
Le ciel est bleu

The model returned the following embedding.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fmultilingual-embeddings.png&w=3840&q=75)

Notice that the model managed to identify the sentences about the bear, soccer, an apple, and the sky, even if they are in different languages.

# Conclusion

Word and sentence embeddings are the bread and butter of LLMs. They are the basic building block of most language models, since they translate human speak (words) into computer speak (numbers) in a way that captures many relations between words, semantics, and nuances of the language, into equations regarding the corresponding numbers.

Sentence embeddings can be extended to language embeddings, in which the numbers attached to each sentence are language-agnostic. These models are very useful for translation and for searching and understanding text in different languages.
"""
    },
    {
        "lesson_title" : "What is Similarity Between Sentences?",
        "text_content" : """
For large language models, it is crucial to know when two words, or two sentences, are similar or different. This can be a hard problem, but luckily, word and sentence embeddings are very helpful for this task. In this post we go over some different notions of similarity.

For large language models, it is crucial to know when two words, or two sentences, are similar or different. This can be a hard problem, but luckily, word and sentence embeddings are very helpful for this task. In this chapter, we go over some different notions of similarity.

# Similarity between text
Knowing if two words are similar or different is a very important task for every large language model. An even harder problem is knowing if two different sentences are similar or different. Luckily, word and sentence embeddings are very useful for this task.

In the previous chapter, I explained the concept of word embeddings. In a nutshell, a word embedding is an assignment of a list of numbers (vector) to every word, in a way that semantic properties of the word translate into mathematical properties of the numbers. What do we mean by this? For example, two similar words will have similar vectors, and two different words will have different vectors. But most importantly, each entry in the vector corresponding to a word keeps track of some property of the word. Some of these properties can be understandable to humans, such as age, size, gender, etc., but some others could potentially only be understood by the computer. Either way, we can benefit from these embeddings for many useful tasks.

Sentence embeddings are even more powerful, as they assign a vector of numbers to each sentence, in a way that these numbers also carry important properties of the sentence. One of the Cohere embeddings assigns a vector of length 4096 (i.e., a list of 4096 numbers) to each sentence. Furthermore, multilingual embedding does this for sentences in more than 100 languages. In this way, the sentence “Hello, how are you?” and its corresponding French translation, “Bonjour, comment ça va?” will be assigned very similar numbers, as they have the same semantic meaning.

Now that we know embeddings quite well, let’s move on to using them to find similarities. There are two types of similarities we’ll define in this post: dot product similarity and cosine similarity. Both are very similar and very useful to determine if two words (or sentences) are similar.

# Dot Product Similarity
Let’s start with a small example of sentence embedding. For simplicity, let’s consider a dataset of 4 sentences, all movie titles, and an embedding of dimension 2, meaning that each sentence is assigned to two numbers. Let’s say that the embedding is the following:

You’ve Got Mail: [0, 5]
Rush Hour: [6, 5]
Rush Hour 2: [7, 4]
Taken: [7, 0]

Let’s take a closer look at these scores. Would they mean anything? As mentioned before, these scores sometimes mean something that humans can understand, and other times they don’t. In this case, notice that the first score is 0 for You’ve Got Mail, but high for all the other movies. Is there a feature that these three movies have, and that You’ve Got Mail doesn’t? I can think of one: being an action movie. Similarly, the second score is high for You’ve Got Mail, Rush Hour, and Rush Hour 2, but low for Taken. What could this property be? Comedy seems to be one. Therefore, in our embedding, it could well be that the first score is the amount of action in the movie, and the second score is the amount of comedy. The following table represents the embedding.

Now, imagine that we want to find the similarities between these movies. In particular, how similar would you say Taken is from You’ve Got Mail? How similar is Rush Hour to Rush Hour 2? In my opinion, Taken and You’ve Got Mail are very different, and Rush Hour and Rush Hour 2 are very similar. We now need to create a similarity score that is low for the pair [You’ve Got Mail, Taken], and high for the pair [Rush Hour, Rush Hour 2].

Here is one way to create this similarity score. Notice that if two movies are similar, then they must have similar action scores and similar comedy scores. So if we multiply the two action scores, then multiply the two comedy scores, and add them, this number would be high if the scores match. On the other hand, if the scores don’t match very well, the similarity score would be lower. This operation is called the dot product. Let’s see how it works for the two pairs of movies.

- Dot product for the pair [You’ve got mail, Taken] = 0*7 + 5*0 = 0
- Dot product for the pair [Rush Hour, Rush Hour 2] = 6*7 + 5*4 = 62

This matches our intuition since we were expecting a low similarity for the first pair, and a high similarity for the second pair.

# Cosine Similarity

Another measure of similarity between sentences (and words) is to look at the angle between them. For example, let’s plot the movie embedding in the plane, where the horizontal axis represents the action score, and the vertical axis represents the comedy score. The embedding looks like this.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fsimilarity-movies.png&w=3840&q=75)

Notice that You’ve Got Mail is quite far from Taken, which makes sense since they are very different movies. Furthermore, Rush Hour and Rush Hour 2 are very close, as they are similar movies. So Euclidean distance (the length of the line between the points) is a good measure for similarity. We need to tweak it a little bit, since we want a measure of similarity that is high for sentences that are close to each other, and low for sentences that are far away from each other. Distance does the exact opposite. So in order to tweak this metric, let’s look at the angle between the rays from the origin (the point with coordinates [0,0]), and each sentence. Notice that this angle is small if the points are close to each other, and large if the points are far away from each other. Now we need the help of another function, the cosine. The cosine of angles close to zero is close to 1, and as the angle grows, the cosine decreases. This is exactly what we need. Therefore, we define the cosine distance as the cosine of the angle formed by the two rays going from the origin, to the two sentences.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fsimilarity-score-1.png&w=3840&q=75)

Notice that in the ongoing example, the angle between the movies You’ve Got Mail, and Taken, is 90 degrees, with a cosine of 0. Therefore, the similarity between them is 0. On the other hand, the angle between the movies Rush Hour and Rush Hour 2 is 11.31 degrees. Its cosine is 0.98, which is quite high. In fact, the similarity between a sentence and itself is always 1, as the angle is 0, with a cosine of 1.

# Real Life Example
Of course, this was a very small example. Let’s do a real-life example with the Cohere embedding.

To set up, we first import several tools we'll need.

```
import numpy as np
import seaborn as sns
import altair as alt
from sklearn.metrics.pairwise import cosine_similarity
```

We also import the Cohere module and create a client.

```
import cohere
co = cohere.ClientV2("COHERE_API_KEY") # Get your free API key: https://dashboard.cohere.com/api-keys
```

Consider the following 3 sentences, stored in the Python list texts.

```
texts = ["I like to be in my house", 
         "I enjoy staying home", 
         "the isotope 238u decays to 206pb"]
```
One would expect the two first sentences to have a high similarity score when compared to each other, and the third one to have a very low similarity score when compared to the other two.

To get the corresponding sentence embeddings, we call the Embed endpoint with co.embed(). We supply three parameters:
- texts - our list of sentences
- model - the model name
- input_type - we use search_document to indicate that we intend to use the embeddings for search use-cases

You'll learn about these parameters in more detail in the LLMU Module on Text Representation.

```
response = co.embed(
    texts=texts,
    model='embed-v4.0',
    input_type='search_document',
    embedding_types=['float']
)
```

The embeddings are stored in the embeddings value of the response. After getting the embeddings, we separate them by sentence and print the values.

```
embeddings = response.embeddings.float

[sentence1, sentence2, sentence3] = embeddings

print("Embedding for sentence 1", np.array(sentence1))
print("Embedding for sentence 2", np.array(sentence2))
print("Embedding for sentence 3", np.array(sentence3))
```

The results are as follows:
```
Embedding for sentence 1 [ 0.04968262  0.03799438 -0.02963257 ... -0.0737915  -0.0079422
 -0.01863098]
Embedding for sentence 2 [ 0.043396    0.05401611 -0.02461243 ... -0.06216431 -0.0196228
 -0.00948334]
Embedding for sentence 3 [ 0.0243988   0.00712967 -0.04669189 ... -0.03903198 -0.02403259
  0.01942444]
```

Note that the embeddings are vectors (lists) of 1024 numbers, so they are truncated here (thus the dots in between). One would expect that the vectors corresponding to sentences 1 and 2 are similar to each other and that both are different from the vector corresponding to sentence 3. However, from inspection, this is not very clear. We need to calculate some similarities to see if this is the case.

# Dot Product Similarity
Let’s calculate the dot products between the three sentences. The following line of code will do it.

```
print("Similarity between sentences 1 and 2:", np.dot(sentence1, sentence2))
print("Similarity between sentences 1 and 3:", np.dot(sentence1, sentence3))
print("Similarity between sentences 2 and 3:", np.dot(sentence2, sentence3))
```

And the results are:
```
Similarity between sentences 1 and 2: 0.818827121924668
Similarity between sentences 1 and 3: 0.19770800712384107
Similarity between sentences 2 and 3: 0.19897217756830138
```

The similarity between sentences 1 and 2 (0.8188) is much larger than the similarities between the other pairs. This confirms our predictions.

Just for consistency, we also calculate the similarities between each sentence and itself, to confirm that a sentence and itself has the highest similarity score.

```
Similarity between sentences 1 and 1: 0.9994656785851899
Similarity between sentences 2 and 2: 1.0006820582016114
Similarity between sentences 3 and 3: 1.0005095878377965
```

This checks out—the similarity between a sentence and itself is around 1, which is higher than all the other similarities.

# Cosine Similarity
Now let’s calculate the cosine similarities between them.

```
print("Cosine similarity between sentences 1 and 2:", cosine_similarity([sentence1], [sentence2])[0][0])  
print("Cosine similarity between sentences 1 and 3:", cosine_similarity([sentence1], [sentence3])[0][0])  
print("Cosine similarity between sentences 2 and 3:", cosine_similarity([sentence2], [sentence3])[0][0])
```

The results are the following:
```
Cosine similarity between sentences 1 and 2: 0.818766792354783
Cosine similarity between sentences 1 and 3: 0.1977104790996451
Cosine similarity between sentences 2 and 3: 0.19885369669720415
```

Next, we check the cosine similarity between each sentence and itself.

```
Cosine similarity between sentences 1 and 1: 0.9999999999999998
Cosine similarity between sentences 2 and 2: 1.0000000000000004
Cosine similarity between sentences 3 and 3: 1.0000000000000004
```

We also plot the results in a grid.
![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fsimilarity-visualize.png&w=3840&q=75)

The similarity between each sentence and itself is 1 (the diagonal in the plot), which is consistent with our expectations. Furthermore, a sentence and itself represent the same point in space, which gives an angle of 0 with the origin, so it makes sense that the similarity is the cosine of 0, which is 1!

Notice that the dot product and cosine distance give nearly identical values. The reason for this is that the embedding is normalized (meaning each vector has norm equal to 1). When the embedding is not normalized, the dot product and cosine distance would give different values.

# Conclusion
In the previous chapter, we learned that sentence embeddings are the bread and butter of language models, as they associate each sentence with a particular list of numbers (a vector), in a way that similar sentences give similar vectors. We can think of embeddings as a way to locate each sentence in space (a high dimensional space, but a space nonetheless), in a way that similar sentences are located close by. Once we have each sentence somewhere in space, it’s natural to think of distances between them. And an even more intuitive way to think of distances is to think of similarities, i.e., a score assigned to each pair of sentences, which is high when these sentences are similar, and low when they are different. The similarity is a very useful concept in large language models, as it can be used for search, for translation, for summarization, and in many other applications. To learn more about these applications, stay tuned for the next article!
        """
    },
    {
        "lesson_title" : "What Is Attention in Language Models?",
        "text_content" : """
A huge roadblock for language models is when a word can be used in two different contexts. When this problem is encountered, the model needs to use the context of the sentence in order to decipher which meaning of the word to use. This is precisely what self-attention models do.

In the previous chapters, you learned about word and sentence embeddings and similarity between words and sentences. In short, a word embedding is a way to associate words with lists of numbers (vectors) in such a way that similar words are associated with numbers that are close by, and dissimilar words with numbers that are far away from each other. A sentence embedding does the same thing, but associating a vector to every sentence. Similarity is a way to measure how similar two words (or sentences) are, by assigning large numbers to words (sentences) that are similar, and small numbers to those that are different.

However, word embeddings have a huge Achilles heel: words that have more than one definition. If a word embedding assigns a vector to, say, the word ‘bank’, it assigns the same vector to all the definitions of ‘bank’. What if you want to use this word in different contexts? Here is where attention comes into play. Self-attention was introduced in the seminal paper Attention is All you Need, written by several co-authors, including Cohere’s cofounder Aidan Gomez. Attention is a very clever way to tell words apart when they are used in different contexts (which turns word embeddings into contextualized word embeddings).

# One Word, Multiple Meanings

In order to understand attention, let’s look at two sentences:

- Sentence 1: The bank of the river.
- Sentence 2: Money in the bank.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fattention.png&w=3840&q=75)

How would a computer know that the word “bank” in the first sentence refers to a setting in nature, and in the second sentence to a financial setting? Well, let’s ask a simpler question: How would a human know this? How did you figure out these two settings? The way you and I did it was probably to look at the neighbouring words. In the first sentence, the word “river” was the one that hinted at the nature setting, and in the second sentence, the word “money” was key to the financial setting. So in short, we need a way to use the other words in the sentence to understand what context of the word “bank” we want to use.

Here is where word embeddings come into play. As you learned in a previous chapter, word embeddings are a way to assign vectors (lists of numbers) to each word. I like to imagine them geometrically. Imagine that the words “bank”, “river”, and “money” are all attached on a cork board. Furthermore, this cork board contains all the existing words, and in such a way that two words that are similar (such as “apple” and “pear”) are close by. Now, in this cork board, “bank”, “river”, and “money” are not exactly close by. However, what you do is take the word “bank”, and move it slightly towards the word “river”. Call this word “bank1”. Now, take another copy of the word “bank”, and move it slightly towards the word “money”. Call this one “bank2”. Now, consider the following two modified sentences.

- Modified sentence 1: The bank1 of the river.
- Modified sentence 2: Money in the bank2.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fattention-bank.png&w=3840&q=75)

In these two sentences, the computer now knows a little more about the context of the word “bank”, as the word has been split into two distinct ones. One whose definition is closer to “river”, and another one whose definition is closer to “money”. That, in short, is how attention mechanisms work. However, there may be many questions lingering in your head. For example:
- What do you mean by “moving a word closer to another one”?
- Why did you ignore the other words in the sentence? How did you know the words “river” and “money” were the ones dictating the context, instead of the words “the”, “in”, or “of”? As humans, we know which words provide context, but a computer wouldn’t have a clue.
- As computers only handle numbers, how do we attach numbers to all these methods?

All these (and hopefully more!) questions will be answered next.

# Moving Words on the Cork Board

First, let me tell you what I mean by “moving a word closer to another one”. The way I like to imagine this, is to average two words. For example, let’s say that I want to move the word “bank” 10% closer to the word river. I now think of the word “0.9_Bank + 0.1_River”. That is, “bank1” is 90% “bank”, and 10% “river”. Also, let’s say that “bank2” is 80% “bank” and 20% “money”. So let’s say these are the modified words:

- Bank1 = 0.9*Bank + 0.1*River
- Bank2 = 0.8*Bank + 0.2*Money

How did I come up with the numbers 0.9, 0.1, 0.8, and 0.2? That comes later (ok I have to spoil it, the answer is similarity, but I’ll elaborate later in this chapter). For now, you may be wondering what do I mean by 0.9*Bank + 0.1*River. Well, in the embeddings chapter, we learned that a word embedding consists of assigning a vector (list) of numbers to each word. The Cohere embedding associates each word with a vector of length 4096 (that is, a list of 4096 numbers per word). For simplicity, let’s imagine an embedding that associates a vector of two numbers to each word, and that the following are the numbers:
- River: [0,5]
- Money: [8,0]
- Bank: [6,6]

These two numbers can be interpreted as coordinates in the plane, where the first number is the horizontal coordinate, and the second one, the vertical coordinate. This gives a graphic like the one below.

So in order to calculate the embeddings of Bank1 and Bank2, we simply do the math componentwise (that means, for each of the two components of the vector, separately). We get this:
- Bank1: 0.9*Bank + 0.1*River = 0.9*[6, 6] + 0.1*[0, 5]
  [5.4, 5.4] + [0, 0.5]
  [5.4, 5.9]
- Bank2: 0.8_Bank + 0.2_Money = 0.8*[6,6] + 0.2*[8,0]
  = [4.8, 4.8] + [1.6, 0]
  = [6.4, 4.8]

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fattention-cork-board.png&w=3840&q=75)

As you can see, “bank1” is closer to “river”, and “bank2” is closer to “money”. As a matter of fact, “bank1” is on the line between “bank” and “river”, 10% along the way. Similarly, “bank2” is on the line between “bank” and “money”, 20% along the way.

Thus, the attention mechanism managed to split the word “bank” into two words, and use each one in the corresponding sentence. You may still have some questions, however, such as the following one.

# How to Decide Which Words Determine Context?

In other words, why did I pick the words “river” and “money” instead of “the”, “of”, and “in”, in order to determine the context of “bank”. Obviously the answer is “because I’m human and I know the language”. But what can the computer do? It can rely on two mechanisms, one of them is a metric such as similarity, which you learned in the previous chapter. The second one is multi-head attention, which we'll talk about at the end of the chapter.

Let’s first discuss the similarity mechanism. What the computer is going to do is to consider all the words in the sentence as context, including irrelevant words such as “the”, “of”, and “in”. However, it’s going to consider them a certain amount, and that amount is precisely the similarity between the word, and “bank”. We trust that in a good embedding, the similarity between “bank” and a word such as “the” is almost zero, as they are unrelated. Therefore, the model will know to ignore these words, and focus on those that may have a higher similarity with the word “bank”.

But let me add some numbers to this reasoning to make it more clear. Imagine that we calculate similarities for the words in each sentence, and we get the following:

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fsimilarity-scores.png&w=3840&q=75)

This similarity makes sense in the following ways:
- The similarity between each word and itself is 1.
- The similarity between any irrelevant word (“the”, “of”, etc.) and any other word is 0.
- The similarity between “bank” and “river” is 0.11.
- The similarity between “bank” and “money” is 0.25.

Why is the similarity between “bank” and “money” higher than the similarity between “bank” and “river”. We can imagine that “bank” gets used more often in the same context as “money”, than as “river”, and that explains the difference. We are simplifying this model quite a bit, it could be that the similarity between “the” and “of” is not zero, but 0.001. However, to simplify our calculations, we’ll use these numbers.

Now, on to the next step. We are going to use the similarities to transform each of the words of this sentence. We’ll call these new words “the1”, “bank1”, “of1”, “river1” for the first sentence, and “money2”, “in2”, “the2”, “bank2” for the second sentence. Beware, we’ll be doing some math with words, but it won’t be very different from the one we did before. Let’s look at the first sentence, “The bank of the river”, and the word “the”. The similarities with the other words are as follows:

Similarities with “the”:

- the: 1
- bank: 0
- of: 0
- river: 0

Therefore, we turn the word “the” into the new word “the1”, which corresponds to the sum 1*“the” + 0*”bank” + 0*”of” + 0*”river”. This is equal to the word “the”. That means, the word “the” doesn’t change, and it’s equal to “the1”.

Now, let’s follow the same procedure with the word “bank”, and see what we get. The similarities of the word “bank” with the other words of the sentence “The bank of the river” are the following:
- the: 0
- bank: 1
- of: 0
- river: 0.11

Therefore, the word “bank” turns into the word “bank1”, given by the equation 1_”bank” + 0.11_”river”. We are almost done. We want the coefficients of the word to add to 1, so we can divide everything by their sum, which is 1.11. When we do that, we get that the word “bank” gets transformed into the word 0.9*”bank” + 0.1”river”.

Let’s do one more for consistency. The word “money” in the second sentence turns into “money2”, given by the equation 1*”money” + 0.25*”bank”. When we normalize, we divide everything by 1.25, to get the equation 0.8*”money” + 0.2*”bank”. All these equations are summarized in the table below.

This is the way we obtained the modified words that we use in the attention mechanism above. The modified sentences then become the following:

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F10%2Foriginal-modified-sentences-1.png&w=3840&q=75)

# Is There More to Attention?
What you learned in this chapter is simple self-attention. However, we can do much better than that. There is a method called multi-head attention, in which one doesn't only consider one embedding, but several different ones. These are all obtained from the original by transforming it in different ways. Multi-head attention has been very successful at the task of adding context to text. If you'd like to learn more about the self and multi-head attention, you can check out the following two videos:

# Conclusion
In this post, you learned what attention mechanisms are. They are a very useful method that helps give words the context coming from the sentence where they belong. In this way, the model has less chance of getting confused by words taken out of context. LLMs make great use of attention mechanisms in order to understand text.
"""},
    {
        "lesson_title" : "What Are Transformer Models and How Do They Work?",
        "text_content" : """
Transformer models are one of the most exciting new developments in machine learning. They were introduced in the paper Attention is All You Need. Transformers can be used to write stories, essays, poems, answer questions, translate between languages, chat with humans, and they can even pass exams that are hard for humans! But what are they? You’ll be happy to know that the architecture of transformer models is not that complex, it simply is a concatenation of some very useful components, each of which has its own function. In this chapter, you will learn all of these components.

In a nutshell, what does a transformer do? Imagine that you’re writing a text message on your phone. After each word, you may get three words suggested to you. For example, if you type “Hello, how are”, the phone may suggest words such as “you”, or “your” as the next word. Of course, if you continue selecting the suggested word in your phone, you’ll quickly find that the message formed by these words makes no sense. If you look at each set of 3 or 4 consecutive words, it may make sense, but these words don’t concatenate to anything with a meaning. This is because the model used in the phone doesn’t carry the overall context of the message, it simply predicts which word is more likely to come up after the last few. Transformers, on the other hand, keep track of the context of what is being written, and this is why the text that they write makes sense.

The phone can suggest the next word to use in a text message, but does not have the power to generate coherent text.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F06%2Fthe-phone-can-suggest-the-next-word.png&w=3840&q=75)

I have to be honest with you, the first time I found out that transformers build text one word at a time, I couldn’t believe it. First of all, this is not how humans form sentences and thoughts. We first form a basic thought, and then start refining it and adding words to it. This is also not how ML models do other things. For example, images are not built this way. Most neural network based graphical models form a rough version of the image, and slowly refine it or add detail until it is perfect. So why would a transformer model build text word by word? One answer is, because that works really well. A more satisfying one is that because transformers are so incredibly good at keeping track of the context, that the next word they pick is exactly what it needs to keep going with an idea.

And how are transformers trained? With a lot of data, all the data on the internet, in fact. So when you input the sentence “Hello, how are” into the transformer, it simply knows that, based on all the text in the internet, the best next word is “you”. If you were to give it a more complicated command, say, “Write a story.”, it may figure out that a good next word to use is “Once”. Then it adds this word to the command, and figures out that a good next word is “upon”, and so on. And word by word, it will continue until it writes a story.

Command: Write a story.
Response: Once

Next command: Write a story. Once
Response: upon

Next command: Write a story. Once upon
Response: a

**Next command: Write a story. Once upon a
**Response:** time

**Next command: Write a story. Once upon a time
**Response:** there

etc.

Now that we know what transformers do, let’s get to their architecture. If you’ve seen the architecture of a transformer model, you may have jumped in awe like I did the first time I saw it, it looks quite complicated! However, when you break it down into its most important parts, it’s not so bad. The transformer has 4 main parts:
- Tokenization
- Embedding
- Positional encoding
- Transformer block (several of these)
- Softmax

The fourth one, the transformer block, is the most complex of all. Many of these can be concatenated, and each one contains two main parts: The attention and the feedforward components.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Ftransformer-architecture.png&w=3840&q=75)

Let’s study these parts one by one.

# Tokenization
Tokenization is the most basic step. It consists of a large dataset of tokens, including all the words, punctuation signs, etc. The tokenization step takes every word, prefix, suffix, and punctuation signs, and sends them to a known token from the library.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Ftokenization.png&w=3840&q=75)

For example, if the sentence is “Write a story”, then the 4 corresponding tokens will be <Write>, <a>, <story>, and \<.>.

# Embedding
Once the input has been tokenized, it’s time to turn words into numbers. For this, we use an embedding. In a previous chapter, you learned about how text embeddings send every piece of text to a vector (a list) of numbers. If two pieces of text are similar, then the numbers in their corresponding vectors are similar to each other (componentwise, meaning each pair of numbers in the same position is similar). Otherwise, if two pieces of text are different, then the numbers in their corresponding vectors are different.

For example, if the sentence we are considering is “Write a story.” and the tokens are <Write>, <a>, <story>, and \<.>, then each one of these will be sent to a long vector, and we’ll have four vectors.
![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fembeddings.png&w=3840&q=75)

# Positional encoding

Once we have the vectors corresponding to each of the tokens in the sentence, the next step is to turn all these into one vector to process. The most common way to turn a bunch of vectors into one vector is to add them, componentwise. That means, we add each coordinate separately. For example, if the vectors (of length 2) are [1,2], and [3,4], their corresponding sum is [1+3, 2+4], which equals [4, 6]. This can work, but there’s a small caveat. Addition is commutative, meaning that if you add the same numbers in a different order, you get the same result. In that case, the sentence “I’m not sad, I’m happy” and the sentence “I’m not happy, I’m sad”, will result in the same vector, given that they have the same words, except in different order. This is not good. Therefore, we must come up with some method that will give us a different vector for the two sentences. Several methods work, and we’ll go with one of them: positional encoding. Positional encoding consists of adding a sequence of predefined vectors to the embedding vectors of the words. This ensures we get a unique vector for every sentence, and sentences with the same words in different order will be assigned different vectors. In the example below, the vectors corresponding to the words “Write”, “a”, “story”, and “.” become the modified vectors that carry information about their position, labeled “Write (1)”, “a (2)”, “story (3)”, and “. (4)”.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fpositional-encoding-1.png&w=3840&q=75)

Now that we know we have a unique vector corresponding to the sentence, and that this vector carries the information on all the words in the sentence and their order, we can move to the next step.

# Transformer block

Let’s recap what we have so far. The words come in and get turned into tokens (tokenization), tokenized words are turned into numbers (embeddings), then order gets taken into account (positional encoding). This gives us a vector for every token that we input to the model. Now, the next step is to predict the next word in this sentence. This is done with a really really large neural network, which is trained precisely with that goal, to predict the next word in a sentence.

We can train such a large network, but we can vastly improve it by adding a key step: the attention component. Introduced in the seminal paper Attention is All you Need, it is one of the key ingredients in transformer models, and one of the reasons they work so well. Attention is explained in the previous section, but for now, imagine it as a way to add context to each word in the text.

The attention component is added at every block of the feedforward network. Therefore, if you imagine a large feedforward neural network whose goal is to predict the next word, formed by several blocks of smaller neural networks, an attention component is added to each one of these blocks. Each component of the transformer, called a transformer block, is then formed by two main components:
- The attention component.
- The feedforward component.

The transformer is a concatenation of many transformer blocks.
![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Ftransformer-block.png&w=3840&q=75)

# Attention
The next step is attention. As you learned in the previous chapter, the attention mechanism deals with a very important problem: the problem of context. Sometimes, as you know, the same word can be used with different meanings. This tends to confuse language models, since an embedding simply sends words to vectors, without knowing which definition of the word they’re using.

Attention is a very useful technique that helps language models understand the context. In order to understand how attention works, consider the following two sentences:

- Sentence 1: The bank of the river.
- Sentence 2: Money in the bank.

As you can see, the word ‘bank’ appears in both, but with different definitions. In sentence 1, we are referring to the land at the side of the river, and in the second one to the institution that holds money. The computer has no idea of this, so we need to somehow inject that knowledge into it. What can help us? Well, it seems that the other words in the sentence can come to our rescue. For the first sentence, the words ‘the’, and ‘of’ do us no good. But the word ‘river’ is the one that is letting us know that we’re talking about the land at the side of the river. Similarly, in sentence 2, the word ‘money’ is the one that is helping us understand that the word ‘bank’ is now referring to the institution that holds money.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fattention-1.png&w=3840&q=75)

In short, what attention does is it moves the words in a sentence (or piece of text) closer in the word embedding. In that way, the word “bank” in the sentence “Money in the bank” will be moved closer to the word “money”. Equivalently, in the sentence “The bank of the river”, the word “bank” will be moved closer to the word “river”. That way, the modified word “bank” in each of the two sentences will carry some of the information of the neighboring words, adding context to it.

The attention step used in transformer models is actually much more powerful, and it’s called multi-head attention. In multi-head attention, several different embeddings are used to modify the vectors and add context to them. Multi-head attention has helped language models reach much higher levels of efficacy when processing and generating text.

# The Softmax Layer
Now that you know that a transformer is formed by many layers of transformer blocks, each containing attention and a feedforward layer, you can think of it as a large neural network that predicts the next word in a sentence. The transformer outputs scores for all the words, where the highest scores are given to the words that are most likely to be next in the sentence.

The last step of a transformer is a softmax layer, which turns these scores into probabilities (that add to 1), where the highest scores correspond to the highest probabilities. Then, we can sample out of these probabilities for the next word. In the example below, the transformer gives the highest probability of 0.5 to “Once”, and probabilities of 0.3 and 0.2 to “Somewhere” and “There”. Once we sample, the word “once” is selected, and that’s the output of the transformer.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F07%2Fsoftmax-layer-1.png&w=3840&q=75)

Now what? Well, we repeat the step. We now input the text “Write a story. Once” into the model, and most likely, the output will be “upon”. Repeating this step again and again, the transformer will end up writing a story, such as “Once upon a time, there was a …”.

# Post Training
Now that you know how transformers work, we still have a bit of work to do. Imagine the following: You ask the transformer “What is the capital of Algeria?”. We would love for it to answer “Algiers”, and move on. However, the transformer is trained on the entire internet. The internet is a big place, and it’s not necessarily the best question/answer repository. Many pages, for example, would have long lists of questions without answers. In this case, the next sentence after “What is the capital of Algeria?” could be another question, such as “What is the population of Algeria?”, or “What is the capital of Burkina Faso?”. The transformer is not a human who thinks about their responses, it simply mimics what it sees on the internet (or any dataset that has been provided). So how do we get the transformer to answer questions?

The answer is post-training. In the same way that you would teach a person to do certain tasks, you can get a transformer to perform tasks. Once a transformer is trained on the entire internet, then it is trained again on a large dataset which corresponds to lots of questions and their respective answers. Transformers (like humans), have a bias towards the last things they’ve learned, so post-training has proven a very useful step to help transformers succeed at the tasks they are asked to.

Post-training also helps with many other tasks. For example, one can post-train a transformer with large datasets of conversations, in order to help it perform well as a chatbot, or to help us write stories, poems, or even code.

# More
As mentioned above, this is a conceptual introduction to give you an idea of how transformers generate text. If you'd like to open the hood and get a more detailed intuition of the mathematics behind a transformer, we invite you to check out the following articles and video by our course instructors, Jay Alammar, and Luis Serrano.

- ![The Illustrated Transformer](https://youtu.be/-QH8fRhqFHM)
- ![How GPT3 Works](https://youtu.be/qaWMOYf4ri8)

# Conclusion
In this chapter you’ve learned how transformers work. They are formed by several blocks, each one with its own function, working together to understand the text and generate the next word. These blocks are the following:
- Tokenizer: Turns words into tokens.
- Embedding: Turns tokens into numbers (vectors)
- Positional encoding: Adds order to the words in the text.
- Transformer block: Guesses the next word. It is formed by an attention block and a feedforward block.
- Attention: Adds context to the text.
- Feedforward: Is a block in the transformer neural network, which guesses the next word.
- Softmax: Turns the scores into probabilities in order to sample the next word.

The repetition of these steps is what writes the amazing text you’ve seen transformers create. The main reason they work so well is because they have a huge amount of parameters that can capture many aspects of the context. We’re excited to see what you can build using transformer models!

"""
    },
    {
        "lesson_title" : "Introduction to Text Embeddings",
        "text_content" : """
We take a visual approach to gain an intuition behind text embeddings, what use cases they are good for, and how they can be customized using finetuning.

We’ll use Cohere’s Python SDK for the code examples. Follow along in this notebook.

When you hear about large language models (LLMs), probably the first thing that comes to mind is the text generation capability, such as writing an essay or creating marketing copy.

Another thing you can get is text representation: a set of numbers that represent what the text means and capture the semantics of the text. These numbers are called text embeddings.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F2b13b38-image.png&w=3840&q=75)

Text generation outputs text, while text representation outputs embeddings

Text embeddings give you the ability to turn unstructured text data into a structured form. With embeddings, you can compare two or more pieces of text, be it single words, sentences, paragraphs, or even longer documents. And since these are sets of numbers, the ways you can process and extract insights from them are limited only by your imagination.

What does this bring? It opens up many possible use cases that apply in the real world today. Embeddings power applications we interact with on a daily basis, such as modern search engines, eCommerce product recommendations, social media content moderation, email spam filtering, customer support conversational agents, and many more.

In this chapter, we take a visual approach to understand the intuition behind text embeddings.

# Step-by-Step Guide
To set up, we first import several tools. We'll use the same notebook for the next several chapters, and we'll import everything we need here.

```
import pandas as pd
import numpy as np
import altair as alt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
```

We also import the Cohere module and create a client.

```
import cohere
co = cohere.ClientV2("COHERE_API_KEY") # Get your free API key: https://dashboard.cohere.com/api-keys
```

## Step 1: Prepare the Dataset
We'll work a subset of the Airline Travel Information System (ATIS) intent classification dataset [Source]. The following code loads the dataset into a pandas Dataframe df with a single column "queries" containing 91 inquiries coming to airline travel inquiry systems.

```
# Load the dataset to a dataframe
df_orig = pd.read_csv('https://raw.githubusercontent.com/cohere-ai/notebooks/main/notebooks/data/atis_intents_train.csv', names=['intent','query'])

# Take a small sample for illustration purposes
sample_classes = ['atis_airfare', 'atis_airline', 'atis_ground_service']
df = df_orig.sample(frac=0.1, random_state=30)
df = df[df.intent.isin(sample_classes)]
df_orig = df_orig.drop(df.index)
df.reset_index(drop=True,inplace=True)

# Remove unnecessary column 
intents = df['intent'] #save for a later need
df.drop(columns=['intent'], inplace=True)
```

Here are a few example data points:
```
- which airlines fly from boston to washington dc via other cities
- show me the airlines that fly between toronto and denver
- show me round trip first class tickets from new york to miami
- i'd like the lowest fare from denver to pittsburgh
- show me a list of ground transportation at boston airport
- show me boston ground transportation
- of all airlines which airline has the most arrivals in atlanta
- what ground transportation is available in boston
- i would like your rates between atlanta and boston on september third
- which airlines fly between boston and pittsburgh
```

## Step 2: Turn Text into Embeddings
Next, we embed each inquiry by calling Cohere’s Embed endpoint with co.embed(). It takes in texts as input and returns embeddings as output. We supply three parameters:

- texts: The list of texts you want to embed
- model: The model to use to generate the embedding.
- input_type — Specifies the type of document to be embedded. At the time of writing, there are four options:
    - search_document: For documents against which search is performed
    - search_query: For query documents
    - classification: For when the embeddings will be used as an input to a text classifier
    - clustering: For when you want to cluster the embeddings

```
def get_embeddings(texts, model="embed-v4.0", input_type="search_document"):
    output = co.embed(
        texts=texts, 
        model=model, 
        input_type=input_type, 
        embedding_types=["float"]
    )
    return output.embeddings.float

df['query_embeds'] = get_embeddings(df['query'].tolist())
```

For every piece of text passed to the Embed endpoint, a sequence of 1024 numbers will be generated. Each number represents a piece of information about the meaning contained in that piece of text.

## Step 3: Visualize Embeddings with a Heatmap
Let’s get some visual intuition about this by plotting these numbers in a heatmap. What we can do is compress the dimension to a much lower number, say 10.

The get_pc() function below does this via a technique called Principal Component Analysis (PCA), which reduces the number of dimensions in an embedding while retaining as much information as possible. We set embeds_pc to the ten-dimensional version of the document embeddings.

```
# Function to return the principal components
def get_pc(arr, n):
    pca = PCA(n_components=n)
    embeds_transform = pca.fit_transform(arr)
    return embeds_transform
  
# Reduce embeddings to 10 principal components to aid visualization
embeds = np.array(df['query_embeds'].tolist())
embeds_pc = get_pc(embeds, 10)
```

We’ll use the 9 data point above as examples and display their compressed embeddings on a heatmap. We have each data point on the y-axis and its corresponding set of 10 embedding values on the x-axis, which looks like this:

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F2604a6e-image.png&w=3840&q=75)

A heatmap showing 10-dimensional embeddings of 9 data points

There are some patterns emerging. To see this, let’s look at a smaller number of examples.

Take these three for example. They are all inquiries about ground transportation in Boston. And by visual inspection, we can see that their embedding patterns are very similar.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2Fa3157ed-image.png&w=3840&q=75)

The 10-dimensional embeddings of 3 inquiries, all about ground transportation in Boston

Now, compare them to the other kinds of inquiries, such as those related to airline information (see two examples below). Notice that while the embeddings about ground transportation inquiries look very similar to each other, they are distinctive from the rest.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F31f890b-image.png&w=3840&q=75)

The 10-dimensional embeddings of 2 inquiries about other matters

Here, the model was able to capture the context and meaning of each piece of text, and it then represents them as embeddings. Each dimension of an embedding, called a feature, represents a certain universal characteristic of text according to how the model understands it.

How is this possible? A large language model has been pre-trained with a vast amount of text data, where the training objective is set up in such a way as to encourage the model to extract contextual information about a piece of text and store it as embeddings.

## Step 4: Visualize Embeddings on a 2D Plot
We can investigate this further by compressing the embeddings to two dimensions and plotting them on a scatter plot. What we would expect is that texts of similar meaning would be closer to each other, and vice versa.

Do note that as we compress the embeddings to lower dimensions, the information retained becomes lesser. However, humans can only visualize in 2D or 3D, and it turns out this is still a good enough approximation to help us gain intuition about the data.
![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2Fd2cd5b2-Screenshot_2024-03-29_at_1.37.12_PM.png&w=3840&q=75)

A plot showing 2D embeddings of 9 data points

By visual inspection, we can see that texts of similar meaning are indeed located close together. We see inquiries about tickets on the left, inquiries about airlines somewhere around the middle, and inquiries about ground transportation on the top right.

These kinds of insights enable various downstream analyses and applications, such as topic modeling, by clustering documents into groups. In other words, text embeddings allow us to take a huge corpus of unstructured text and turn it into a structured form, making it possible to objectively compare, dissect, and derive insights from all that text.

In the coming chapters, we'll dive deeper into these topics.

# Conclusion
In this chapter you learned about the Embed endpoint. Text embeddings make possible a wide array of downstream applications such as semantic search, clustering, and classification. You'll learn more about those in the subsequent chapters.
        """
    
    },
    {
        "lesson_title" : "Introduction to Text Generation",
        "text_content" : """
Chatbots brought large language models (LLMs) into the mainstream. LLMs have been around for a few years, but their adoption was largely limited to the AI community. The launch of AI-powered consumer chatbots has made LLMs accessible to the everyday user, and now they're a hot topic in tech and enterprise circles alike.

This text generation module teaches you how to build LLM chatbots using Cohere’s Chat endpoint.

# Command Model
Command is Cohere’s flagship LLM. It generates a response given a prompt or message from a user. It is trained to follow user commands and to be instantly useful in practical business applications, like summarization, copywriting, extraction, and question answering.

Command has been trained with a large volume of multi-turn conversations to ensure that it excels at the various nuances associated with conversational language. It ranks at the top of the Holistic Evaluation of Language Models (HELM) benchmark, an evaluation leaderboard comparing large language models on a wide number of tasks (March ‘23 results).

# Command R and Command R+ Models

Command R and Command R+ are designed to be the market leading family of models in the ‘scalable’ category that balance high efficiency with strong accuracy to enable enterprises to move from proof of concept into production-grade AI.

Here are some key features of Command R:

- High-performance RAG: Retrieval-augmented generation (RAG) enables enterprises to give the model access to private knowledge that it otherwise would not have.
- Access to tools: Tool use enables enterprise developers to turn Command R into an engine for powering the automation of tasks and workflows that require using internal infrastructure like databases and software tools, as well as external tools like CRMs, search engines, and more. Command R+ supports Multi-Step Tool Use which allows the model to combine multiple tools over multiple steps to accomplish difficult tasks.
- Low latency and high throughput: Command R targets the “scalable” category of models that balance high performance with strong accuracy, enabling companies to move beyond proof of concept and into production.
- 128k context length and lower pricing: Command R features a longer context length, supporting up to 128k tokens in its initial release.
- Strong capabilities across 10 key languages: The model excels at 10 major languages for global business: English, French, Spanish, Italian, German, Portuguese, Japanese, Korean, Arabic, and Chinese.
- Model weights available for research and evaluation: Cohere For AI is releasing the weights for this version of Command R publicly, so that it can be used for research purposes.

# How an LLM Chatbot Works
To understand how LLM chatbots work, it’s important to develop an understanding of their building blocks. This section focuses on how to build the generative part of a chatbot by looking at how to use a foundational model and added layers of context to generate answers in a conversation style.

# The Foundation of an LLM Chatbot
The foundation of an LLM chatbot is an LLM that has been fine-tuned to follow instructions. It can generate a response given a prompt or message from a user. This type of model is tuned to follow instructions and questions, such as “Write a headline for my homemade jewelry product” or “What is the capital of Canada?”.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F47e24b4-message-and-response-2.png&w=3840&q=75)

However, the LLM’s context is limited to only the last message it receives, and it does not consider any previous messages and responses.

Yet, chatbots are characterized by their ability to maintain a conversation with a user, which takes place over multiple interactions.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F4980442-baseline-llm-context.png&w=3840&q=75)

The goal of a chatbot is to solve this problem by linking a sequence of interactions into a single instance, allowing the chatbot to hold an ongoing conversation. In doing so, the model’s response can keep a memory of all the previous interactions instead of having to start from scratch every time.


# How to Build a Chatbot's Memory

Working off of the baseline generation model above, we can layer together multiple interactions into a single prompt and create a memory of the entire conversation.

First, we add a system-level prompt called a preamble. A preamble contains instructions to help steer a chatbot’s response toward specific characteristics, such as a persona, style, or format. For example, if we want the chatbot to adopt a formal style, the preamble can be used to encourage the generation of more business-like and professional responses. The preamble could be something like "You are a helpful chatbot, trained to assist human users by providing responses in a formal and professional tone."

Then, we append the current user message to the preamble, which becomes the prompt for the chatbot’s response. Next, we append the chatbot response and the following user message to the prompt.

We can repeat this step for any number of interactions until we reach the model’s maximum context length. Context length is the total number of tokens taken up by the prompt and response, and each model has a maximum context length that it can support.
        
![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2F4d798fc-building-a-conversation.png&w=3840&q=75)

This multi-turn framework is what gives chatbots the ability to hold the full context of conversation from start to finish.

![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2Fbc73d3f-multi-turn-conversations-2.png&w=3840&q=75)

However, building on top of a baseline LLM alone is not sufficient.

Chatbots need to perform well in a wide range of scenarios. To create a robust chatbot that consistently generates high-quality and reliable output, the baseline LLM needs to be adapted specifically to conversations. This means taking the baseline model and fine-tuning it further with a large volume of conversational data.

This is what forms the foundation of Cohere’s Chat endpoint — let’s take a closer look.

# Cohere's Chat Endpoint
Improving LLM chatbot performance starts with how the baseline LLM is trained. The model powering the Chat endpoint is Cohere’s Command model, trained with a large volume of multi-turn conversations. This ensures that the model will excel at the various nuances associated with conversational language and perform well across different use cases.

Beyond training, fine-tuning a baseline LLM for conversations requires adding a standardized interface on top of the prompt formatting system. The Chat endpoint provides a consistent, simplified, and structured way of handling the prompt formatting that defines how the prompt inputs should be organized, making it easier for developers to build chatbot applications. This added layer includes a fixed abstraction and schema, providing more stability to scale and build applications on top of the foundation model.

The Chat endpoint includes all the elements required for an LLM chatbot (as discussed in the previous sections), exposing a simple interface for developers. It consists of the following key components:

- Preamble management: Developers can opt to use the endpoint’s default preamble or override it with their own preambles.
- Multi-turn conversations: The Chat endpoint builds upon the Command model by enabling multi-turn conversations.
- State management: State management preserves the conversation memory. Developers can either leverage the endpoint’s conversation history persistence feature or manage the conversation history themselves.
- Fully-managed conversation: The abstraction layer of the Chat endpoint means there’s only one item to send to the API: the user message. Everything else is managed automatically. At the same time, developers who want greater control over a chatbot’s configuration can still do so.
        
![image](https://cohere.com/_next/image?url=https%3A%2F%2Fcohere-ai.ghost.io%2Fcontent%2Fimages%2F2024%2F05%2Fad2e6eb-the-chat-endpoint-exposes-a-simple-interface-4.png&w=3840&q=75)

# Conclusion
Cohere's Command model and Chat endpoint offer powerful tools for developers looking to harness the potential of LLMs in their applications. Command's capabilities, coupled with the Chat endpoint's developer-friendly interface, allow developers to build text generation applications across diverse business applications.     
        """
    }
]


QUIZZES = [
    {
       "lesson_title" : "What Are Word and Sentence Embeddings?",
       "quiz_title" : "What Are Word and Sentence Embeddings?",
       "quiz_questions" : [
            {
                "question" : "What is the fundamental challenge that word and sentence embeddings help solve?",
                "options" : [
                    "Making computers faster at processing language",
                    "Bridging the gap between human language (words) and computer language (numbers)",
                    "Translating between different human languages",
                    "Improving speech recognition accuracy"
                ],
                "correct_answer" : 2
            },
            {
                "question" : "In a good word embedding, what relationship should exist between similar words?",
                "options" : [
                    "They should have identical numerical representations",
                    "They should be assigned to points that are close to each other",
                    "They should have completely different numerical values",
                    "They should always be positioned along the same axis"
                ],
                "correct_answer" : 2
            },
            {
                "question" : "What important property do good word embeddings capture beyond simple word similarity?",
                "options" : [
                    "The historical origins of words",
                    "The pronunciation patterns of words",
                    "Relationships and analogies between words",
                    "The frequency of word usage in common texts"
                ],
                "correct_answer" : 3
            },
            {
                "question" : "Imagine you're explaining word embeddings to a friend. Which real-life analogy would best help them understand?",
                "options" : [
                    "A dictionary where words are listed alphabetically",
                    "A map where similar restaurants are clustered in the same neighborhoods",
                    "A random number generator",
                    "A calendar organizing events by date"
                ],
                "correct_answer" : 2
            }
        ]
    },
    {
        "lesson_title" : "What is Similarity Between Sentences?",
        "quiz_title" : "What is Similarity Between Sentences?",
        "quiz_questions" : [
            {
                "question" : "Why are embeddings useful for large language models?",
                "options" : [
                    "They provide rules for grammar",
                    "They help calculate similarities between words or sentences",
                    "They translate text into speech",
                    "They detect typos in text"
                ],
                "correct_answer" : 2
            },
            {
                "question" : "Word embeddings assign a single number to each word to capture its meaning. True or False?",
                "options" : [
                    "True",
                    "False"
                ],
                "correct_answer" : 2
            },
            {
                "question" : "In dot product similarity, what happens when two vectors point in the same direction and have high values?",
                "options" : [
                    "The dot product is zero",
                    "The dot product is negative",
                    "The dot product is high",
                    "They are considered dissimilar"
                ],
                "correct_answer" : 3
            },
            {
                "question" : "Which measure looks at the angle between two vectors rather than their magnitude?",
                "options" : [
                    "Dot product",
                    "Cosine similarity",
                    "Euclidean distance",
                    "Manhattan distance"
                ],
                "correct_answer" : 2
            }
        ]
    },
    {
        "lesson_title" : "What Is Attention in Language Models?",
        "quiz_title" : "What Is Attention in Language Models?",
        "quiz_questions" : [
            {
                "question" : "What is the main limitation of traditional word embeddings like Word2Vec or GloVe?",
                "options" : [
                    "They are too long to compute",
                    "They require labeled data",
                    "They assign the same vector to a word regardless of context",
                    "They are only used in speech recognition"
                ],
                "correct_answer" : 3
            },
            {
                "question" : "What does self-attention do in a language model?",
                "options" : [
                    "It randomly changes word meanings",
                    "It finds grammatical errors",
                    "It uses context to adjust word meanings dynamically",
                    "It removes stop words like “the” or “of”"
                ],
                "correct_answer" : 3
            },
            {
                "question" : "In the context of self-attention, why is the word “bank” problematic?",
                "options" : [
                    "It has no vector representation",
                    "It is a slang term",
                    "It has multiple meanings depending on context",
                    "It is too similar to other finance terms"
                ],
                "correct_answer" : 3
            },
            {
                "question" : "Suppose the word 'bat' appears in two sentences:\n'The bat flew in the night.'\n'He hit the ball with a bat.' Which words would self-attention most likely rely on to disambiguate the meaning of 'bat'?",
                "options" : [
                    "'the', 'in', 'with'",
                    "'flew', 'night', 'ball', 'hit'",
                    "'a', 'he', 'the'",
                    "None of the above"
                ],
                "correct_answer" : 2
            }
        ]
    }
]