from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

# Set Downlaod Location for Huggingface
os.environ['HF_HOME'] = "/tmp"

documents = [
    # The Declaration of Independence
    """We hold these truths to be self-evident, that all men are created equal,
    that they are endowed by their Creator with certain unalienable Rights, that
    among these are Life, Liberty and the pursuit of Happiness. That to secure
    these rights, Governments are instituted among Men, deriving their just
    powers from the consent of the governed.""",

    # Abraham Lincoln, Gettysburg Address
    """Four score and seven years ago our fathers brought forth on this
    continent, a new nation, conceived in Liberty, and dedicated to the
    proposition that all men are created equal. Now we are engaged in a great
    civil war, testing whether that nation, or any nation so conceived and so
    dedicated, can long endure.""",

    # Henry David Thoreau, Civil Disobedience
    """I heartily accept the motto, “That government is best which governs
    least”; and I should like to see it acted up to more rapidly and
    systematically. Carried out, it finally amounts to this, which also I
    believe—“That government is best which governs not at all”; and when men
    are prepared for it, that will be the kind of government which they will
    have.""",

    # James Madison, Federalist No. 10
    """Among the numerous advantages promised by a well-constructed Union, none
    deserves to be more accurately developed than its tendency to break and
    control the violence of faction. The friend of popular governments never
    finds himself so much alarmed for their character and fate as when he
    contemplates their propensity to this dangerous vice.""",

    # Henry David Thoreau, Walden
    """I went to the woods because I wished to live deliberately, to front only
    the essential facts of life, and see if I could not learn what it had to
    teach, and not, when I came to die, discover that I had not lived. I did not
    wish to live what was not life, living is so dear; nor did I wish to
    practise resignation, unless it was quite necessary.""",

    # Herman Melville, Moby-Dick
    """Whenever I find myself growing grim about the mouth; whenever it is a
    damp, drizzly November in my soul; whenever I find myself involuntarily
    pausing before coffin warehouses, and bringing up the rear of every funeral
    I meet; and especially whenever my hypos get such an upper hand of me, that
    it requires a strong moral principle to prevent me from deliberately
    stepping into the street, then, I account it high time to get to sea as soon
    as I can.""",

    # Mary Shelley, Frankenstein
    """Learn from me, if not by my precepts, at least by my example, how
    dangerous is the acquirement of knowledge, and how much happier that man is
    who believes his native town to be the world, than he who aspires to become
    greater than his nature will allow.""",

    # Francis Bacon, Of Studies
    """Studies serve for delight, for ornament, and for ability. Their chief use
    for delight is in privateness and retiring; for ornament, is in discourse;
    and for ability, is in the judgment and disposition of business. For expert
    men can execute, and perhaps judge of particulars, one by one; but the
    general counsels, and the plots and marshalling of affairs, come best from
    those that are learned.""",

    # William Shakespeare, Hamlet
    """To be, or not to be, that is the question: Whether ’tis nobler in the
    mind to suffer the slings and arrows of outrageous fortune, or to take arms
    against a sea of troubles, and by opposing end them. To die, to sleep—no
    more—and by a sleep to say we end the heart-ache and the thousand natural
    shocks that flesh is heir to: ’tis a consummation devoutly to be wished.""",

    # Charles Dickens, A Tale of Two Cities
    """It was the best of times, it was the worst of times, it was the age of
    wisdom, it was the age of foolishness, it was the epoch of belief, it was
    the epoch of incredulity, it was the season of Light, it was the season of
    Darkness, it was the spring of hope, it was the winter of despair, we had
    everything before us, we had nothing before us.""",
]

embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")


query = "A government should not boss upon it's citizens"

doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embeddings)[0]

relevant_document = documents[max(list(enumerate(scores)),key=lambda x: x[1])[0]]

print(relevant_document)