from tkinter import *
import pandas as pd


def analyser(option):
    letter_frequency_data = pd.read_csv("average_letter_frequency.csv")
    eng_alphabet = letter_frequency_data["ENG"][:26].to_list()
    ukr_alphabet = letter_frequency_data["UKR"][:33].to_list()
    alphabet = 0
    if eng_language.get() and ukr_language.get():
        alphabet, average_freq, analyser_results = eng_alphabet + ukr_alphabet, \
                                                   letter_frequency_data["ENG_FREQ"][:26].to_list() + \
                                                   letter_frequency_data["UKR_FREQ"][:33].to_list(), \
                                                   letter_frequency_data["ENG_FREQ_USING_ANALYSER"][:26].to_list() + \
                                                   letter_frequency_data["UKR_FREQ_USING_ANALYSER"][:33].to_list()
    elif eng_language.get():
        alphabet, average_freq, analyser_results = eng_alphabet, letter_frequency_data["ENG_FREQ"][:26].to_list(), \
                                                   letter_frequency_data["ENG_FREQ_USING_ANALYSER"][:26].to_list()
    elif ukr_language.get():
        alphabet, average_freq, analyser_results = ukr_alphabet, letter_frequency_data["UKR_FREQ"][:33].to_list(), \
                                                   letter_frequency_data["UKR_FREQ_USING_ANALYSER"][:33].to_list()
    else:
        output_scope.delete("1.0", END)
        output_scope.insert(END, "PLEASE SELECT LANGUAGE")

    if alphabet != 0:
        text = input_scope.get("1.0", END)
        if text.isspace():
            output_scope.delete("1.0", END)
            output_scope.insert(END, "INSERT SOME TEXT PLEASE")
        else:
            letter_amount_dict = dict.fromkeys(alphabet, 0)
            amount_of_chars = 0
            for letter in text.upper():
                if letter in alphabet:
                    letter_amount_dict[letter] += 1
                    amount_of_chars += 1

            df = pd.DataFrame(list(letter_amount_dict.items()), columns=["Letter", "Amount"])
            df["Text Frequency"] = round(100 * df["Amount"] / amount_of_chars, 3)

            if compare_with_average_frequency.get() and compare_with_analyzer_results.get():
                df["Average Frequency"] = average_freq
                df["Deviation (aver freq)"] = round(abs(df["Text Frequency"] - df["Average Frequency"]), 3)
                df["Frequency based on analyser results"] = analyser_results
                df["Deviation (analyzer results)"] = round(abs(df["Text Frequency"] -
                                                               df["Frequency based on analyser results"]), 3)
            elif compare_with_average_frequency.get():
                df["Average Frequency"] = average_freq
                df["Deviation"] = round(abs(df["Text Frequency"] - df["Average Frequency"]), 3)
            elif compare_with_analyzer_results.get():
                df["Frequency based on analyser results"] = analyser_results
                df["Deviation"] = round(abs(df["Text Frequency"] - df["Frequency based on analyser results"]), 3)

            if sort_by.get() == "frequency":
                df = df.sort_values(by='Text Frequency', ascending=False)

            if option == "output":
                output_scope.delete("1.0", END)
                output_scope.insert(END, df.to_string(index=False))
            if option == "save":
                df.to_csv("frequency_table.csv", index=False, encoding="utf-8-sig")
                file_with_analyzed_text = open("analyzed_text.txt", "w", encoding="utf-8-sig")
                file_with_analyzed_text.write(text)
                output_scope.delete("1.0", END)
                output_scope.insert(END, "Check 'frequency_table.csv' and 'analyzed_text.txt':)")


def clear_canvas():
    input_scope.delete("1.0", END)
    output_scope.delete("1.0", END)


window = Tk()
window.geometry("1160x720")
window.title("Frequency analysis of the text")

input_scope = Text(window, bg="#FCF9FF", fg="#9272AE", selectbackground="#9272AE",
                   padx=6, pady=4, font=("Ubuntu Mono", 12), wrap=NONE)
xscrollbar_input = Scrollbar(input_scope, orient=HORIZONTAL)
xscrollbar_input.config(command=input_scope.xview)
input_scope.configure(xscrollcommand=xscrollbar_input.set)
xscrollbar_input.pack(side=BOTTOM, fill=X)

output_scope = Text(window, bg="#FCF9FF", fg="#9272AE", selectbackground="#9272AE",
                    padx=6, pady=4, font=("Ubuntu Mono", 12), wrap=NONE)
xscrollbar_output = Scrollbar(output_scope, orient=HORIZONTAL)
xscrollbar_output.config(command=output_scope.xview)
output_scope.configure(xscrollcommand=xscrollbar_output.set)
xscrollbar_output.pack(side=BOTTOM, fill=X)

eng_language, ukr_language = IntVar(), IntVar()
Checkbutton(window, text="ENG", var=eng_language, font=("Century Gothic", 8), fg="#775D8E").place(x=28, y=660)
Checkbutton(window, text="UKR", var=ukr_language, font=("Century Gothic", 8), fg="#775D8E").place(x=28, y=680)

sort_by = StringVar(value=0)
Radiobutton(window, text="frequency", var=sort_by, value="frequency",
            font=("Century Gothic", 8), fg="#775D8E").place(x=158, y=660)
Radiobutton(window, text="alphabetical order", var=sort_by, value="alphabetical order",
            font=("Century Gothic", 8), fg="#775D8E").place(x=158, y=680)

compare_with_average_frequency, compare_with_analyzer_results = IntVar(), IntVar()
Checkbutton(window, text="average frequency", var=compare_with_average_frequency,
            font=("Century Gothic", 8), fg="#775D8E").place(x=308, y=660)
Checkbutton(window, text="frequency based on analyzer results", var=compare_with_analyzer_results,
            font=("Century Gothic", 8), fg="#775D8E").place(x=308, y=680)

analyze_button = Button(window, text="ANALYZE", font=("Century Gothic", 11), bg="#F8EDF3", fg="#D9559A",
                        relief="ridge", command=lambda: analyser("output"))
clear_input_button = Button(window, text="<", font=("Century Gothic", 11), bg="#EDF6F8", fg="#7DB2BD",
                            relief="ridge", command=lambda: input_scope.delete("1.0", END))
clear_both_button = Button(window, text="<>", font=("Century Gothic", 11), bg="#EDF6F8", fg="#7DB2BD",
                           relief="ridge", command=lambda: clear_canvas())
clear_output_button = Button(window, text=">", font=("Century Gothic", 11), bg="#EDF6F8", fg="#7DB2BD",
                             relief="ridge", command=lambda: output_scope.delete("1.0", END))
save_button = Button(window, text="SAVE", font=("Century Gothic", 11), bg="#F4E9F7", fg="#775D8E",
                     relief="ridge", command=lambda: analyser("save"))
exit_button = Button(window, text="EXIT", font=("Century Gothic", 11, "bold"), bg="#F4E9F7", fg="#775D8E",
                     relief="ridge", command=window.destroy)

Label(window, text="Insert text to analyze:", font=("Century Gothic", 13), fg="#503E5F").place(x=28, y=13)
Label(window, text="CLEAR", font=("Century Gothic", 11), fg="#7DB2BD").place(x=553, y=304)
Label(window, text="Analysis table:", font=("Century Gothic", 13), fg="#503E5F").place(x=628, y=13)
Label(window, text="Select language/s:", font=("Century Gothic", 8), fg="#503E5F").place(x=30, y=644)
Label(window, text="Sort by:", font=("Century Gothic", 8), fg="#503E5F").place(x=160, y=644)
Label(window, text="Compare text frequency with:", font=("Century Gothic", 8), fg="#503E5F").place(x=310, y=644)

input_scope.place(x=30, y=40, height=600, width=500)
clear_input_button.place(x=540, y=330, height=25, width=25)
clear_both_button.place(x=565, y=330, height=25, width=30)
clear_output_button.place(x=595, y=330, height=25, width=25)
analyze_button.place(x=540, y=375, height=40, width=80)
output_scope.place(x=630, y=40, height=600, width=500)
save_button.place(x=960, y=660, height=40, width=75)
exit_button.place(x=1054, y=660, height=40, width=75)

mainloop()
