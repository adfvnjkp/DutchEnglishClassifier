from CalculateMethod import *
import sys
import pickle


def loading(filepath: str) -> tuple:
    """
    helper func load data from set file
        return tuple, list holding all instance of Sentence class, int hold length of list
    :param filepath:
    :return: list of Sentence instances

    """
    sentenceList = []
    content = open(filepath, encoding="utf-8")
    for line in content:
        sentence = Sentence(line.strip().split("|")[0], line.strip().split("|")[1])
        sentenceList.append(sentence)

    return sentenceList, len(sentenceList)


def paramInvalid(errMsg: str):
    """
    helper func handle all invalid param read from commandline
    :return: not requested

    """
    # prompt error msg
    print("! Please type in Valid param according to prompt !" + "\n" + errMsg)
    # exit program halt further computation
    exit(-2)


def restoring(modelpath: str) -> object:
    """"""
    # restore dumped object
    fpin = open(modelpath, "rb")
    modelObj = pickle.load(fpin)
    return modelObj


def serialization(modelObj: object, modelpath: str):
    """
    helper func serialization of file
    :param modelObj: model treated as object
    :param modelpath: model path specified
    :return: not specified

    """
    # dump in location
    fput = open(modelpath, "wb")
    pickle.dump(modelObj, fput)
    # close handle
    fput.close()


def main():
    """
    param read from commandline
        param[1] -> "train"
            param[2] -> "ad" / "dt"
            param[3] -> path for train file storage: "./dataRepo/size_10000.dat"
            param[4] -> location for model serialization: "./serialization/model"
        param[1] -> "predict"
            param[2] -> path for test file storage: "./dataRepo/size_10000.dat"
            param[3] -> path for model serialization storage: "./serialization/model_dt" / "./serialization/model_ad"
        possible param  -> train:
                                python Entrance.py "train" "dt" "./dataRepo/size_10000.dat" "./serialization/model"
                        -> predict:
                                python Entrance.py "predict" "./dataRepo/size_10000.dat" "./serialization/model_dt"
    """
    # var initialization
    matched = 0
    # read in task as train
    if sys.argv[1] == "train":
        # load train file
        fpath = sys.argv[3]
        sentenceList, amount = loading(fpath)
        # train type
        if sys.argv[2] == "dt":
            # initialization for dt
            columnList = [index for index in range(10)]
            # build return tree root
            root = dtBuild(sentenceList, columnList)
            modelOutput = sys.argv[4] + "_dt"
            serialization(root, modelOutput)
        elif sys.argv[2] == "ad":
            # build return stumps with weights
            stumpNodes, stumpWeights = adBuild(sentenceList, 50)
            modelOutput = sys.argv[4] + "_ad"
            serialization((stumpNodes, stumpWeights), modelOutput)
        else:
            paramInvalid("train ad / dt instruction")

    # read in task as predict
    elif sys.argv[1] == "predict":
        # load test file
        fpath = sys.argv[2]
        mpath = sys.argv[3]
        sentenceList, amount = loading(fpath)
        # check predict model by name, if "dt" found
        if "dt" in mpath.split("_"):
            # model restoring
            root = restoring(mpath)
            for sentence in sentenceList:
                res = dtPredict(sentence, root)
                if res == sentence.language:
                    matched += 1
            # output correctness
            print("correctness of prediction: " + str(float(matched / amount)))
        # if predicted by "ad" specified
        elif "ad" in mpath.split("_"):
            # model restoring
            stumpNodes, stumpWeights = restoring(mpath)
            for sentence in sentenceList:
                res = adPredict(sentence, stumpNodes, stumpWeights)
                if res == sentence.language:
                    matched += 1
            # output correctness
            print("correctness of prediction: " + str(float(matched / amount)))

        else:
            paramInvalid("! predict ad / dt instruction !")

    else:
        paramInvalid("! train / predict instruction !")


if __name__ == '__main__':
    main()