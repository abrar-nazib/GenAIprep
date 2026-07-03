from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model1 = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0,
)

model2 = ChatOpenRouter(
    model="qwen/qwen3.5-flash-02-23",
    temperature=0,
)

prompt1 = PromptTemplate(
    template="Generate short and simple notes from the following text\n{text}",
    input_variables=["text"]
)

prompt2 = PromptTemplate(
    template="Generate 5 short questions and answers from the following text\n{text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="Merge the provided notes and quiz into a single document\n\nNotes:\n{notes}\n\nQuiz:\n{quiz}",
    input_variables=["notes", "quiz"]
)

parser = StrOutputParser()

# Create parallel chain
parallel_chain = RunnableParallel({
    "notes": prompt1 | model1 | parser,
    "quiz" : prompt2 | model2 | parser

})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text = """1.17.1. Multi-layer Perceptron
Multi-layer Perceptron (MLP) is a supervised learning algorithm that learns a function
 by training on a dataset, where
 is the number of dimensions for input and
 is the number of dimensions for output. Given a set of features
 and a target
, it can learn a non-linear function approximator for either classification or regression. It is different from logistic regression, in that between the input and the output layer, there can be one or more non-linear layers, called hidden layers. Figure 1 shows a one hidden layer MLP with scalar output.

../_images/multilayerperceptron_network.png
Figure 1 : One hidden layer MLP.
The leftmost layer, known as the input layer, consists of a set of neurons
 representing the input features. Each neuron in the hidden layer transforms the values from the previous layer with a weighted linear summation
, followed by a non-linear activation function
 - like the hyperbolic tan function. The output layer receives the values from the last hidden layer and transforms them into output values.

The module contains the public attributes coefs_ and intercepts_. coefs_ is a list of weight matrices, where weight matrix at index
 represents the weights between layer
 and layer
. intercepts_ is a list of bias vectors, where the vector at index
 represents the bias values added to layer
.

1.17.2. Classification
Class MLPClassifier implements a multi-layer perceptron (MLP) algorithm that trains using Backpropagation.

MLP trains on two arrays: array X of size (n_samples, n_features), which holds the training samples represented as floating point feature vectors; and array y of size (n_samples,), which holds the target values (class labels) for the training samples:

from sklearn.neural_network import MLPClassifier
X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y)
MLPClassifier(alpha=1e-05, hidden_layer_sizes=(5, 2), random_state=1,
              solver='lbfgs')
After fitting (training), the model can predict labels for new samples:

clf.predict([[2., 2.], [-1., -2.]])
array([1, 0])
MLP can fit a non-linear model to the training data. clf.coefs_ contains the weight matrices that constitute the model parameters:

[coef.shape for coef in clf.coefs_]
[(2, 5), (5, 2), (2, 1)]
Currently, MLPClassifier supports only the Cross-Entropy loss function, which allows probability estimates by running the predict_proba method.

MLP trains using Backpropagation. More precisely, it trains using some form of gradient descent and the gradients are calculated using Backpropagation. For classification, it minimizes the Cross-Entropy loss function, giving a vector of probability estimates
 per sample
:

clf.predict_proba([[2., 2.], [1., 2.]])
array([[1.967e-04, 9.998e-01],
       [1.967e-04, 9.998e-01]])
MLPClassifier supports multi-class classification by applying Softmax as the output function.

Further, the model supports multi-label classification in which a sample can belong to more than one class. For each class, the raw output passes through the logistic function. Values larger or equal to 0.5 are rounded to 1, otherwise to 0. For a predicted output of a sample, the indices where the value is 1 represent the assigned classes of that sample:

X = [[0., 0.], [1., 1.]]
y = [[0, 1], [1, 1]]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(15,), random_state=1)

clf.fit(X, y)
MLPClassifier(alpha=1e-05, hidden_layer_sizes=(15,), random_state=1,
              solver='lbfgs')
clf.predict([[1., 2.]])
array([[1, 1]])
clf.predict([[0., 0.]])
array([[0, 1]])
See the examples below and the docstring of MLPClassifier.fit for further information.

Examples

Compare Stochastic learning strategies for MLPClassifier

See Visualization of MLP weights on MNIST for visualized representation of trained weights.

1.17.3. Regression
Class MLPRegressor implements a multi-layer perceptron (MLP) that trains using backpropagation with no activation function in the output layer, which can also be seen as using the identity function as activation function. Therefore, it uses the square error as the loss function, and the output is a set of continuous values.

MLPRegressor also supports multi-output regression, in which a sample can have more than one target.

1.17.4. Regularization
Both MLPRegressor and MLPClassifier use parameter alpha for regularization (L2 regularization) term which helps in avoiding overfitting by penalizing weights with large magnitudes. Following plot displays varying decision function with value of alpha.

../_images/sphx_glr_plot_mlp_alpha_001.png
See the examples below for further information.

Examples

Varying regularization in Multi-layer Perceptron

1.17.5. Algorithms
MLP trains using Stochastic Gradient Descent, Adam, or L-BFGS. Stochastic Gradient Descent (SGD) updates parameters using the gradient of the loss function with respect to a parameter that needs adaptation, i.e.



where
 is the learning rate which controls the step-size in the parameter space search.
 is the loss function used for the network.

More details can be found in the documentation of SGD

Adam is similar to SGD in a sense that it is a stochastic optimizer, but it can automatically adjust the amount to update parameters based on adaptive estimates of lower-order moments.

With SGD or Adam, training supports online and mini-batch learning.

L-BFGS is a solver that approximates the Hessian matrix which represents the second-order partial derivative of a function. Further it approximates the inverse of the Hessian matrix to perform parameter updates. The implementation uses the Scipy version of L-BFGS.

If the selected solver is ‘L-BFGS’, training does not support online nor mini-batch learning.

1.17.6. Complexity
Suppose there are
 training samples,
 features,
 hidden layers, each containing
 neurons - for simplicity, and
 output neurons. The time complexity of backpropagation is
, where
 is the number of iterations. Since backpropagation has a high time complexity, it is advisable to start with smaller number of hidden neurons and few hidden layers for training.

1.17.7. Tips on Practical Use
Multi-layer Perceptron is sensitive to feature scaling, so it is highly recommended to scale your data. For example, scale each attribute on the input vector X to [0, 1] or [-1, +1], or standardize it to have mean 0 and variance 1. Note that you must apply the same scaling to the test set for meaningful results. You can use StandardScaler for standardization.

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Don't cheat - fit only on training data
scaler.fit(X_train)
X_train = scaler.transform(X_train)
# apply same transformation to test data
X_test = scaler.transform(X_test)
An alternative and recommended approach is to use StandardScaler in a Pipeline

Finding a reasonable regularization parameter
 is best done using GridSearchCV, usually in the range 10.0 ** -np.arange(1, 7).

Empirically, we observed that L-BFGS converges faster and with better solutions on small datasets. For relatively large datasets, however, Adam is very robust. It usually converges quickly and gives pretty good performance. SGD with momentum or nesterov’s momentum, on the other hand, can perform better than those two algorithms if learning rate is correctly tuned.

1.17.8. More control with warm_start
If you want more control over stopping criteria or learning rate in SGD, or want to do additional monitoring, using warm_start=True and max_iter=1 and iterating yourself can be helpful:

X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = MLPClassifier(hidden_layer_sizes=(15,), random_state=1, max_iter=1, warm_start=True)
for i in range(10):
    clf.fit(X, y)
    # additional monitoring / inspection
MLPClassifier(...
"""


result = chain.invoke({"text": text})

print(result)

chain.get_graph().print_ascii()