import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import roc_auc_score as roc_auc

from core.composer.chain import Chain
from core.composer.node import PrimaryNode, SecondaryNode
from core.models.data import InputData, train_test_data_setup
from core.repository.dataset_types import DataTypesEnum
from core.repository.tasks import Task, TaskTypesEnum


def compose_chain() -> Chain:
    chain = Chain()
    node_first = PrimaryNode('svc')
    node_second = PrimaryNode('lda')
    node_third = SecondaryNode('rf')

    node_third.nodes_from.append(node_first)
    node_third.nodes_from.append(node_second)

    chain.add_node(node_third)

    return chain


def get_iris_data() -> InputData:
    synthetic_data = load_iris()
    input_data = InputData(idx=np.arange(0, len(synthetic_data.target)),
                           features=synthetic_data.data,
                           target=synthetic_data.target,
                           task=Task(TaskTypesEnum.classification),
                           data_type=DataTypesEnum.table)
    return input_data


def test_multiclassification_chain_fit_correct():
    data = get_iris_data()
    chain = compose_chain()
    train_data, test_data = train_test_data_setup(data, shuffle_flag=True)

    chain.fit(input_data=train_data)
    results = chain.predict(input_data=test_data)

    roc_auc_on_test = roc_auc(y_true=test_data.target,
                              y_score=results.predict,
                              multi_class='ovo',
                              average='macro')

    assert roc_auc_on_test > 0.95
