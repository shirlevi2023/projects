#ifndef HASHFUNCS_H_
#define HASHFUNCS_H_


#include <string.h>
#include <stdlib.h>

/**
 * Integers simple hash func.
 */
size_t hash_int (const void *elem)
{
  size_t hash = *((int *) elem);
  return hash;
}

/**
 * Chars simple hash func.
 */
size_t hash_char (const void *elem)
{
  if (elem == NULL)
    return 0;
  size_t hash = *((char *) elem);
  return hash;
}

/**
 * Doubles simple hash func.
 */
size_t hash_double (const void *elem)
{
  size_t hash = *((double *) elem);
  return hash;
}

/**
 * Hashes strings based on content and length
 */
size_t hash_str (const void *elem)
{
  char *string = *((char **) elem);
  int len = (int) strlen (string);
  size_t hash = 0;
  for (int i = 0; i < len; ++i)
    {
      hash += string[i];
    }
  hash *= len;
  return hash;
}

#endif // HASHFUNCS_H_