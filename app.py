from tracker import get_hmm_info

if __name__ == "__main__":
    prompt = input("Enter your natural language prompt: ")
    result = get_hmm_info(prompt)
    print("\n✅ Result:")
    print(result)
