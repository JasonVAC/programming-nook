#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    string sentence = "the bad fox jumps over the lazy dog";
    
    cout << "原句: " << sentence << endl << endl;
    
    vector<string> words;
    string word = "";
    for (char c : sentence) {
        if (c == ' ') {
            if (!word.empty()) {
                words.push_back(word);
                word = "";
            }
        } else {
            word += c;
        }
    }
    if (!word.empty()) {
        words.push_back(word);
    }
    
    cout << "单词列表:" << endl;
    for (size_t i = 0; i < words.size(); i++) {
        cout << "  " << i + 1 << ". " << words[i] << endl;
    }
    cout << endl;
    
    string longest = "";
    for (const string& w : words) {
        if (w.size() > longest.size()) {
            longest = w;
        }
    }
    cout << "最长单词: " << longest << " (" << longest.size() << " 个字符)" << endl << endl;
    
    string replaced = sentence;
    size_t pos = replaced.find("bad");
    while (pos != string::npos) {
        replaced.replace(pos, 3, "good");
        pos = replaced.find("bad", pos + 4);
    }
    cout << "替换后: " << replaced << endl << endl;
    
    int vowelCount = 0;
    string vowels = "aeiouAEIOU";
    for (char c : sentence) {
        if (vowels.find(c) != string::npos) {
            vowelCount++;
        }
    }
    cout << "元音数: " << vowelCount << endl << endl;
    
    string reversedSentence = "";
    for (size_t i = 0; i < words.size(); i++) {
        string reversedWord = "";
        for (int j = words[i].size() - 1; j >= 0; j--) {
            reversedWord += words[i][j];
        }
        reversedSentence += reversedWord;
        if (i != words.size() - 1) {
            reversedSentence += " ";
        }
    }
    cout << "反转单词: " << reversedSentence << endl;
    
    return 0;
}

//Joke环节
//int main(){
//  std::cout << "原句: the bad fox jumps over the lazy dog" << std::endl;
//  std::cout << "单词列表:\n" << "1. the\n2. bad\n3. fox\n4. jumps\n5. over\n6. the\n7. lazy\n8. dog" <<std::endl;
//  std::cout << "最长单词: jumps (5 个字符)\n替换后: the good fox jumps over the lazy dog" << std::endl;
//  std::cout << "元音数: 10\n反转单词: eht doog xof spmuj revo eht yzal god\n" << std::endl;
//  return 0;
//}
