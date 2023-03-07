import multiprocessing as mp
import threading

import Levenshtein
import pandas as pd


class LevenDictChecker:
    def __init__(self, dictionary_path: str):
        if dictionary_path.endswith(".csv"):
            self.dictionary = pd.read_csv(dictionary_path)
        elif dictionary_path.endswith(".parquet"):
            self.dictionary = pd.read_parquet(dictionary_path)
        else:
            raise ValueError(f"Invalid dictionary file format: {dictionary_path}")

    def _compare_distance(self, word: str, input_str: str) -> int:
        return Levenshtein.distance(word, input_str)

    # create a method to get only words of a certain length from the dictionary
    def _truncate_dictionary(self, length: int):
        return self.dictionary[self.dictionary["length"] == length]

    def search(self, input_str: str, max_distance: int = 1) -> list:
        """
        Search for words in the dictionary that are within the max_distance of the input_str.
        """
        results = []
        gen_dict = self._truncate_dictionary(len(input_str))
        for i in range(
            len(input_str) - max_distance, len(input_str) + max_distance + 1
        ):
            tmp_dict = self._truncate_dictionary(i)
            # append the truncated dictionary to the general dictionary dataframe with pd.concat
            gen_dict = pd.concat([gen_dict, tmp_dict])

        for word in gen_dict['word']:
            distance = self._compare_distance(word, input_str)
            if distance <= max_distance:
                results.append(word)
                print(f"Found {word} with distance {distance}")
        return results

    def search_parallel(self, input_str: str, max_distance: int = 1) -> list:
        """
        Search for words in the dictionary that are within the max_distance of the input_str.
        """
        results = []
        with mp.Pool() as pool:
            for word in self.dictionary:
                distance = pool.apply_async(
                    self._compare_distance, args=(word, input_str)
                )
                if distance.get() <= max_distance:
                    results.append(word)
        return results

    def save_results_to_txt(self, results: list, output_path: str) -> None:
        with open(output_path, "w") as f:
            for word in results:
                f.write(f"{word}\n")


if __name__ == "__main__":
    ls = LevenDictChecker("data/english_dictionary.parquet")
    # ask for input
    input_str = input("Enter a word: ")
    input_distance = int(input("Enter a distance: "))
    results = ls.search(input_str, input_distance)
    ls.save_results_to_txt(results, "data/results.txt")
