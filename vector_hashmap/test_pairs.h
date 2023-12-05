//
// Created by shiro on 29/05/2021.
//

#ifndef _TEST_PAIRS_H_
#define _TEST_PAIRS_H_


#include <stdlib.h>

#include "pair.h"


pair* create_pair(const_keyT key, const_valueT value);
void *char_key_cpy (const_keyT key);
void *int_value_cpy (const_valueT value);
int char_key_cmp (const_keyT key_1, const_keyT key_2);
int int_value_cmp (const_valueT val_1, const_valueT val_2);
void char_key_free (keyT* key);
void int_value_free (valueT *val);
int is_digit (const_keyT elem);
void double_value (valueT elem);
pair* create_pair_of_int_and_char(const_keyT key, const_valueT value);

/**
 * Copies the char key of the pair.
 */
void *char_key_cpy (const_keyT key)
{
  char *new_char = malloc (sizeof (char));
  *new_char = *((char *) key);
  return new_char;
}

/**
 * Copies the int value of the pair.
 */
void *int_value_cpy (const_valueT value)
{
  int *new_int = malloc (sizeof (int));
  *new_int = *((int *) value);
  return new_int;
}

/**
 * Compares the char key of the pair.
 */
int char_key_cmp (const_keyT key_1, const_keyT key_2)
{
  return *(char *) key_1 == *(char *) key_2;
}

/**
 * Compares the int value of the pair.
 */
int int_value_cmp (const_valueT val_1, const_valueT val_2)
{
  return *(int *) val_1 == *(int *) val_2;
}

/**
 * Frees the char key of the pair.
 */
void char_key_free (keyT* key)
{
  if (key && *key)
    {
      free (*key);
      *key = NULL;
    }
}

/**
 * Frees the int value of the pair.
 */
void int_value_free (valueT *val)
{
  if (val && *val)
    {
      free (*val);
      *val = NULL;
    }
}


/**
 * @param elem pointer to a char (keyT of pair_char_int)
 * @return 1 if the char represents a digit, else - 0
 */
int is_digit (const_keyT elem)
{
  char c = *((char *) elem);
  return (c > 47 && c < 58);
}

/**
 * doubles the value pointed to by the given pointer
 * @param elem pointer to an integer (valT of pair_char_int)
 */
void double_value (valueT elem)
{
  *((int *) elem) *= 2;
}

pair* create_pair_of_int_and_char(const_keyT key, const_valueT value)
{
  pair* pair = pair_alloc ((char*)key, (int*)value, char_key_cpy,
                           int_value_cpy,
                           char_key_cmp, int_value_cmp, char_key_free,
                           int_value_free);
  return pair;

}

pair* create_pair(const_keyT key, const_valueT value)
{
  pair* pair = pair_alloc (&key, &value, int_value_cpy, int_value_cpy,
                           int_value_cmp,
                           int_value_cmp, int_value_free, int_value_free);
  return pair;

}










#endif //_TEST_PAIRS_H_
