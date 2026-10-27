
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

''' PARALLEL CHAIN '''

model1 = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_tokens=1000
)

model2 = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_tokens=1000
)

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template="Generate short and simple notes from the following text \n {text}.",
    input_variables=["text"],
)

prompt2 = PromptTemplate(
    template="Generate 5 questions and answers about the following text: {text}.",
    input_variables=["text"],
)

prompt3 = PromptTemplate(
    template="Merge the provided notes and quiz into a single document: {notes} and {quiz}.",
    input_variables=["notes", "quiz"],
)

parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {
        'notes': prompt1 | model1 | parser,
        'quiz': prompt2 | model2 | parser,
    }
)

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text = """
In machine learning, a neural network (NN) or artificial neural network (ANN) is a computational model inspired by the structure and functions of biological neural networks.[1][2]

A neural network consists of connected units or nodes called artificial neurons, which loosely model the neurons in the brain. These are connected by edges, which model the synapses in the brain. Each artificial neuron receives signals from connected neurons, then processes them and sends a signal to other connected neurons. The "signal" is a real number, and the output of each neuron is computed by some non-linear function of the totality of its inputs, called the activation function. The strength of the signal at each connection is determined by a weight, which adjusts as part of the training process.

Groups of neurons are aggregated into layers. Each layer performs a transformation on its inputs. Signals travel from the first layer (the input layer) to the last layer (the output layer), typically passing through multiple intermediate layers (hidden layers). A network is typically called a deep neural network if it has at least two hidden layers. Deep neural networks are capable of learning sophisticated hierarchical representations.[3]

Training neural networks is a compute-intensive process, accelerated by the use of graphics processing units (GPUs), and large datasets.
"""

result = chain.invoke({"text": text})

print("Result:\n", result)

chain.get_graph().print_ascii()
