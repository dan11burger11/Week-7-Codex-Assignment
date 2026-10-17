## Entry 1
- **date and time:** 10/16/26 8:44 pm
- **Prompt:** load and clean the ameshousing dataset so that we can properly evaluate my prompt regarding the connection between .5 bathroom increases and its effect on home sales price.
- use best judgement to determine what should be done with an observation for full/half bathroom counts or sales prices in the case of missing data, duplicates, inconsistent formatting,
- or any other errors so they have the least impact on my desired evaluation. Create a total bathrooms variable that is the sum of all the individual bathroom variables(including
- basement bathrooms)
- **Explanation:** I accepted the output of Codex because it produced a new, clean csv that solved 2 missing values issues by replacing them with 0s for bathroom count variables. No need
- to modify or reject any of the work because reviewing the Codex response, python cleaning file, and cleaning notes markdown file indicated that my prompt was followed appropriately.

## Entry 2
- **date and time:** 10/16/26 9:01 pm
- **Prompt:** Use the cleaned ameshousing dataset and evaluate to what extent do marginal increases in sales price differ when upgrading from 1 to 1.5 bathrooms versus larger homes
- (such as 2 to 2.5 bathrooms, 3 to 3.5, etc.). Taking a look at the proportional change, which group of homes' sales price are most impacted by the .5 bathroom upgrade? Give me a summary
- table with summary statistics on the variables that relate to my previously stated analytical question. Also give me a visualization that highlights the percentage change in home prices
- with each .5 bathroom increase.
- **Explanation:** I accepted the output of Codex for correctly analyzing the question I posited regarding the change in sales price realtive to the .5 bathroom increase and comparing each
- tier of increase. This produced a helpful .svg histogram that highlighted the variation at each tier. I rejected the csv tables that were made in response to my request for summary
- tables as they were hard to read in their original state. I modified with my next prompt.

## Entry 3
- **date and time:** 10/16/26 9:09 pm
- **Prompt:** could you make markdown tables of the bath price changes csv and bath summary csv so the results are easy to read
- **Explanation:** I accepted the output of Codex because it followed my request and saved markdown table version of what the previously mentioned csvs were trying to indicate in a clean
- manner. This request was a modification of my previous prompt.

## Entry 4
- **date and time:** 10/16/26 9:11 pm
- **Prompt:** can each of these be saved in the week 7 codex assignment folder
- **Explanation:** I accepted this output from Codex because it followed my simple request and succesfully saved the previously created markdown tables created in the terminal and saved
- them to my repository folder. I rejected the creation of them only for me to see in the codex session and modified the request via this prompt to have them saved in my repository
- folder.

## Entry 5
- **date and time:** 10/16/26 9:19 pm
- **Prompt:** Now write a brief narrative in plain language that explains the results from this analysis and what can be gleaned from it. Is there a significant proportional difference
- for each tier (1-1.5 vs 2-2.5, etc.)? Where was the greatest impact vs the smallest?
- **Explanation:** I accepted this output from Codex because it gave me a great summary of the results of the analysis. I also accept the explanation that while there is an obvious
- correlation between the increase in bathrooms and the increase in sales price, there is also a lot more variables that affect the sales price of the homes and the number of bathrooms
- cannot explain the entirety of the variation. 


