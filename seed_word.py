# -*- coding: utf-8 -*-
import pickle
import unicodedata
import re
import numpy as np
from numpy import array
from tqdm import tqdm
from typing import List, Dict, Tuple
from transformers import BertForSequenceClassification, AutoTokenizer, TextClassificationPipeline


def load_dictionary(filepath: str) -> set:
    with open(filepath, 'r', encoding='utf-8') as f:
        words = set(line.strip() for line in f)
    return words


# 단어 사전 경로 설정
dictionary_path = 'word_dictionary.txt'
dictionary = load_dictionary(dictionary_path)

# 캐시 저장소
remove_suffix_cache = {}


def remove_suffix(word: str) -> str:
    if word in remove_suffix_cache:
        return remove_suffix_cache[word]

    # 단어 사전에 있는 경우, 그대로 반환
    if word in dictionary:
        remove_suffix_cache[word] = word
        return word

    # 단어 끝에 있는 한국어 조사 및 어미만 제거
    original_word = re.sub(r'(을|를|은|는|이|가|에|와|과|도|다|로|의|께서|한테|에게|에서|으로|까지|만|부터|나|며|지만|같이|도|라도|마저|밖에|면|든지|니까|요|서|야|네요|어|아|아요|어여|겠|쯤|가량|보다|여|네요|어요|가요|나요|다요|군요|네요|군가|나가|구나|으니까|아서|어서|는데|은데|였|였어요|였구나|이었|으로서|으로써|요|고|죠|라|어라|야|거|서|네|지|죠|어|나|거|기|니|가|어라|야|라도|나마|뿐|랑|던|래요|이라|고|조차|은커녕|는데|더라도|도|마저|밖에|조차|까지|이라도|이야|라서|으니|하다|어때|잖아|으니|거든|따라서|보다는|보다는|서|로서|는지|는가|로|이다|아서|면서|러니|려니|하고|인데|니까|기|가|으|리|였|다|자|니|이|을|라는|는|니다|이|다|라|으로|란|으며|든지|서|까|라도|쯤|만큼|대로|만큼|조차|이라고|한다면|인|이라면|니|라|고|할|하고|도|다가|에게|와|의|에|으로|를|은|이|가|야|은|는|이|가|의|을|를|로|에|을|하다|을|를|야|고|와|과|이|다|로서|하다|으로|를|에서|을|를|을|다|로서|라|니|가|이고|은|는|이|가|을|를)$', '', word)

    # 원형 단어가 사전에 있으면 반환
    if original_word in dictionary:
        remove_suffix_cache[word] = original_word
        return original_word

    # 그렇지 않으면 원래 단어 반환
    remove_suffix_cache[word] = word
    return word


def most_similar(mat: np.ndarray, idx: int, k: int) -> Tuple[np.ndarray, np.ndarray]:
    vec = mat[idx]
    dists = mat.dot(vec) / (np.linalg.norm(mat, axis=1) * np.linalg.norm(vec))
    top_idxs = np.argpartition(dists, -k)[-k:]
    dist_sort_args = dists[top_idxs].argsort()[::-1]
    return top_idxs[dist_sort_args], dists[top_idxs][dist_sort_args]


def get_top_similar(word: str, words: List[str], mat: np.ndarray, k: int = 100) -> Dict[str, float]:
    base_word = remove_suffix(word)
    word_idx = words.index(word)
    sim_idxs, sim_dists = most_similar(mat, word_idx, k + 1)
    words_sim = np.array(words)[sim_idxs[1:]]  # 제외하고 상위 k개 단어
    dists_sim = sim_dists[1:]

    result = {}
    for i in range(len(words_sim)):
        filtered_word = remove_suffix(words_sim[i])
        if filtered_word != base_word and filtered_word not in result:
            result[filtered_word] = dists_sim[i]
            if len(result) >= k:
                break

    return result


def seedword(query_word):
    with open('filtered_valid_nearest.dat', 'rb') as f:
        valid_nearest, valid_nearest_mat = pickle.load(f)

    # print(f"Loaded filtered valid nearest words: {len(valid_nearest)}")
    # query_word = input("유사도를 구할 단어를 입력하세요: ")

    try:
        top_similar = get_top_similar(
            query_word, valid_nearest, valid_nearest_mat, k=20)
        # print(f"\n'{query_word}'와 유사도 상위 20개 단어:")
        word_list = []
        for word, sim in sorted(top_similar.items(), key=lambda x: x[1], reverse=True):
            if word == "아욱죽과" or word == "박영순의" or word == "원두와":
                continue
            word_list.append(word)
        return word_list
    except ValueError as e:
        return str(e)
