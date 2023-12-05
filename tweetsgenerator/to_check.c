#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAX_WORDS_IN_SENTENCE_GENERATION 20
#define MAX_WORD_LENGTH 100
#define MAX_SENTENCE_LENGTH 1000



typedef struct WordStruct {
    char *word;
    struct WordProbability *prob_list;
    int appearnces_at_text;
    size_t capacity;
    int indicator;
} WordStruct;

typedef struct WordProbability {
    struct WordStruct *word_struct_ptr;
    int param;
    int probability;
} WordProbability;

/************ LINKED LIST ************/
typedef struct Node {
    WordStruct *data;
    struct Node *next;
} Node;

typedef struct LinkList {
    Node *first;
    Node *last;
    int size;
} LinkList;


int is_it_unique(char* word, LinkList* dict);
int is_that_a_last_word(const char* str);

LinkList apdate_list (FILE *fptr2, char *buf, LinkList *lst);
int get_num_of_non_last_words (const LinkList *dictionary);
void update_indicator (const char *str, WordStruct *p);
/**
 * Add data to new node at the end of the given link list.
 * @param link_list Link list to add data to
 * @param data pointer to dynamically allocated data
 * @return 0 on success, 1 otherwise
 */
int add(LinkList *link_list, WordStruct *data)
{
  Node *new_node = malloc(sizeof(Node));
  if (new_node == NULL)
    {
      return 1;
    }
  *new_node = (Node){data, NULL};

  if (link_list->first == NULL)
    {
      link_list->first = new_node;
      link_list->last = new_node;
    }
  else
    {
      link_list->last->next = new_node;
      link_list->last = new_node;
    }

  link_list->size++;
  return 0;
}
/*************************************/

/**
 * Get random number between 0 and max_number [0, max_number).
 * @param max_number
 * @return Random number
 */
int get_random_number(int max_number)
{
  int n = rand() % max_number;
  return n;
}

/**
 * Choose randomly the next word from the given dictionary, drawn uniformly.
 * The function won't return a word that end's in full stop '.' (Nekuda).
 * @param dictionary Dictionary to choose a word from
 * @return WordStruct of the chosen word
 */
WordStruct *get_first_random_word(LinkList *dictionary)
{
  Node* tmp = dictionary->first;
  int n = get_num_of_non_last_words (dictionary);
//  printf("%d n is = \n", n);
  int x = get_random_number(n);
//  printf("%d x is = \n", x);
  int i = 0;
  int count = 0;
  while (i < dictionary->size)
    {
      if (tmp->data->indicator)
        {
          i++;
          tmp = tmp->next;
          continue;
        }
      if (count == x)
        {
          return tmp->data;
        }
      count++;
      i++;
      tmp = tmp->next;

    }
  return NULL;

}
int get_num_of_non_last_words (const LinkList *dictionary)
{
  Node* tmp = dictionary->first;
  int count = 0;
  for (int i = 0; i < dictionary->size; ++i)
    {
      if (tmp->data->indicator)
        {
          tmp = tmp->next;

          continue;
        }
      else
        {
          count++;
        }
      tmp = tmp->next;
    }
  return count;
}

/**
 * Choose randomly the next word. Depend on it's occurrence frequency
 * in word_struct_ptr->WordProbability.
 * @param word_struct_ptr WordStruct to choose from
 * @return WordStruct of the chosen word
 */
WordStruct *get_next_random_word(WordStruct *word_struct_ptr)
{
  // if prob is not null!!!
  int capacity = word_struct_ptr->capacity;
  WordProbability* prob_list = word_struct_ptr->prob_list;
  WordProbability* tmp = prob_list;
  int i = 0;
  int num = get_random_number(capacity);
//  printf(" num is = %d\n", num);
  int j = 0;
  int param = prob_list[i].param;
  while (i <= capacity - 1)
    {
      if (num >= j && num < param)
        {
          return prob_list[i].word_struct_ptr;
        }
      else
        {
          j = param;
          param = param + prob_list[i+1].param;
          i++;
        }

    }
  if (i == capacity)
    {
      return prob_list[i-1].word_struct_ptr;
    }

//  int i = 0;
//  int j = 0;
//  while (i < capacity)
//    {
//
//      tmp++;
//      i++;
//    }


}

/**
 * Receive dictionary, generate and print to stdout random sentence out of it.
 * The sentence most have at least 2 words in it.
 * @param dictionary Dictionary to use
 * @return Amount of words in printed sentence
 */
int generate_sentence(LinkList *dictionary)
{
  int i = 0;
  WordStruct* first_word = get_first_random_word(dictionary);
  printf("%s ", first_word->word);
  WordStruct* new_word = get_next_random_word(first_word);
  while (i < MAX_SENTENCE_LENGTH)
    {
      if (new_word->indicator)
        {
          printf("%s", new_word->word);
          return i;

        }
      printf("%s ", new_word->word);
      new_word = get_next_random_word(new_word);
      i++;

    }
  return i;
}

/**
 * Gets 2 WordStructs. If second_word in first_word's prob_list,
 * update the existing probability value.
 * Otherwise, add the second word to the prob_list of the first word.
 * @param first_word
 * @param second_word
 * @return 0 if already in list, 1 otherwise.
 */
int add_word_to_probability_list(WordStruct *first_word, WordStruct  //
// arrive here when a letter appear after another
*second_word)
{
  if (first_word->prob_list == NULL)
    {
      WordProbability* temp = malloc(1 * sizeof(WordProbability));
      if (temp == NULL)
        {
          printf("alloc failed"); // check

          exit(EXIT_FAILURE);
        }
      first_word->prob_list = temp;

      first_word->prob_list[0].param = 1;
      first_word->capacity = 1;
      first_word->prob_list[0].word_struct_ptr = second_word;
      first_word->prob_list[0].probability = first_word->prob_list[0].param;
    }

  else
    { //check if the word2 already exist at word1's lst
      WordProbability* tmp = first_word->prob_list;
      int i = 0;
      while (i < first_word->capacity)
        {
          if (tmp->word_struct_ptr == second_word)
            {
              first_word->prob_list[i].param ++;
              return 0;
            }
          tmp++;
          i++;
        }
      WordProbability* t = realloc(first_word->prob_list,
                                   sizeof(WordProbability)*
                                   (first_word->capacity + 1));
      if (t == NULL)
        {
          printf("alloc failed");
//           free(first_word->prob_list)  // problem with hello and shir
          exit(EXIT_FAILURE);
        }
      first_word->prob_list = t;
      first_word->capacity ++;
      first_word->prob_list[first_word->capacity-1].param = 1;
      first_word->prob_list[first_word->capacity-1].word_struct_ptr =second_word ;
    }







}

/**
 * Read word from the given file. Add every unique word to the dictionary.
 * Also, at every iteration, update the prob_list of the previous word with
 * the value of the current word.
 * @param fp File pointer
 * @param words_to_read Number of words to read from file.
 *                      If value is bigger than the file's word count,
 *                      or if words_to_read == -1 than read entire file.
 * @param dictionary Empty dictionary to fill
 */
void fill_dictionary(FILE *fp, int words_to_read, LinkList *dictionary)
// need func check if its unique word
// if unique - create node and puts the imformation
// this func pass on the file- strtok
{
}

/**
 * Free the given dictionary and all of it's content from memory.
 * @param dictionary Dictionary to free
 */
void free_dictionary(LinkList *dictionary)
{
}

Node* find_word_at_dict(char *str, LinkList* lst)
{
  Node* tmp = lst->first;
  while (tmp != NULL)
    {
      if (strcmp(str, tmp->data->word) == 0)
        {
          return tmp;
        }
      tmp = tmp->next;
    }

  return NULL;
}


int is_it_unique(char* new_word, LinkList* dict)
{
  if (dict->first == NULL)
    {
      return 1;
    }
  Node* head = dict->first;
  Node* tmp = head;
  while (tmp != NULL)
    {
      if (strcmp(tmp->data->word, new_word) == 0)  //if the word already
        // exist at
        // dictionary
        {
          return 0; // it is not unique
        }
      tmp = tmp->next;
    }
  return 1;
}

int is_that_a_last_word(const char* str)
{
  int n = strlen(str);
  if (str[strlen(str) - 1] == '.')
    {
      return 1;
    }
  return 0;
}




/**
 * @param argc
 * @param argv 1) Seed
 *             2) Number of sentences to generate
 *             3) Path to file
 *             4) Optional - Number of words to read
 */
int main(int argc, char *argv[])
{
  FILE* fptr;
  FILE* fptr2;
  char buf[MAX_WORD_LENGTH];
  fptr = fopen( "C:\\Users\\shiro\\CLionProjects\\tweetsgenerator\\mytext"\
                ".txt", "r");

  fptr2 = fopen( "C:\\Users\\shiro\\CLionProjects\\tweetsgenerator\\mytext"\
                ".txt", "r");

  LinkList lst;
  int words_count = 0;
  lst.first = NULL;
  lst.last = NULL;
  lst.size = 0;
  while (fgets(buf, MAX_WORD_LENGTH, fptr) != NULL)
    {
      char* str;
      str = strtok (buf," \n\r");
      while (str != NULL)
        {
          if (is_it_unique(str, &lst))
            {
              WordStruct* p = malloc(sizeof(WordStruct));
              {
                if (p == NULL)
                  {
                    printf("Allocation failure: alloc failed");
                  }
              }
              p->word = malloc(MAX_WORD_LENGTH * sizeof(char)); // check alloc fail!!
              strcpy(p->word, str);
//              printf ("%s\n", p->word);
              p->prob_list = NULL;
              p->capacity = 0;
              p->appearnces_at_text = 1;
              update_indicator (str, p);
              if (add(&lst, p) == 1)
                {
                  free(p->word); // check if need!
                  free(p);
                  printf("Allocation failure: alloc failed");
                  return EXIT_FAILURE;
                }

              //create and update prob lst- save the prev

            }
          else // if is not unique, add it to num of appeareances at txt
            {
              Node *ptr = find_word_at_dict(str, &lst);
              ptr->data->appearnces_at_text ++;
            }


//          prev = str;
//          WordStruct * first_word = (WordStruct *) find_word_at_dict (prev, &lst)->data;
//          WordStruct * second_word = (WordStruct *) find_word_at_dict (str, &lst)->data;
//          add_word_to_probability_list(first_word, second_word);
          str = strtok (NULL, " \n\r"); // if str null?
          words_count++;
        }
    }

  lst = apdate_list (fptr2, buf, &lst);

  printf("size= %d\n", lst.size);
  printf("count= %d\n", words_count);
  srand(time(NULL));
//  int x = get_random_number(n);
  WordStruct* word = get_first_random_word(&lst);
  WordStruct* j = get_next_random_word(lst.first->next->data);
//  printf("%s\n", word->word);
//  printf("word2: %s\n", j->word);
  generate_sentence(&lst);



//ssssssssssssss




  fclose(fptr);





  return 0;
}
void update_indicator (const char *str, WordStruct *p)
{
  if (is_that_a_last_word(str))
    {
      p->indicator = 1;
    }
  else
    {
      p->indicator = 0;
    }
}

LinkList apdate_list (FILE *fptr2, char *buf, LinkList *lst)
{
  char* prev;
  while (fgets(buf, MAX_WORD_LENGTH, fptr2) != NULL)
    {
      char* str2;
      str2 = strtok (buf," \n\r");
      while (str2 != NULL)
        {
          prev = str2;
          str2 = strtok (NULL, " \n\r");
          char* cur = str2;
          if (str2 == NULL)
            {
              break;
            }
          if (is_that_a_last_word(prev) == 1)
            {
              continue;
            }
          WordStruct * first_word = (WordStruct *) find_word_at_dict (prev, lst)->data;
          WordStruct * second_word = (WordStruct *) find_word_at_dict (cur,
                                                                       lst)->data;

          if (add_word_to_probability_list(first_word, second_word) == 0)
            {
              continue;

            }

        }
    }
  return (*lst);
}
