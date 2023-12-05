#ifndef HASHMAP_H_
#define HASHMAP_H_

#include <stdlib.h>
#include "vector.h"
#include "pair.h"


#include "hashmap.h"

/**
 *
 * @def HASH_MAP_INITIAL_CAP
 * The initial capacity of the hash map.
 * It means, the initial number of <b> vectors </b> the hash map has.
 */
#define HASH_MAP_INITIAL_CAP 16UL

/**
 * @def HASH_MAP_GROWTH_FACTOR
 * The growth factor of the hash map.
 * Example: hash_map(size=16),
 *          hash_map.add([16 elements]) ->
 *          hash_map(size=32)
 */
#define HASH_MAP_GROWTH_FACTOR 2UL

/**
 * @def HASH_MAP_MIN_LOAD_FACTOR
 * The minimal load factor the hash map can be in.
 * Example: if the hash_map capacity is 16,
 * and it has 4 elements in it (size is 4),
 * if an element is erased, the load factor drops below 0.25,
 * so the hash map should be minimized (to 8 vectors).
 */
#define HASH_MAP_MIN_LOAD_FACTOR 0.25

/**
 * @def HASH_MAP_MAX_LOAD_FACTOR
 * The maximal load factor the hash map can be in.
 * Example: if the hash_map capacity is 16,
 * and it has 12 elements in it (size is 12),
 * if another element is added, the load factor goes above 0.75,
 * so the hash map should be extended (to 32 vectors).
 */
#define HASH_MAP_MAX_LOAD_FACTOR 0.75

/**
 * @typedef hash_func
 * This type of function receives a keyT and returns
 * a representational number of it.
 * Example: lets say we have a pair
 * ('Joe', 78) that we want to store in the hash map,
 * the key is 'Joe' so it determines the bucket in the hash map,
 * his index would be:  size_t ind = hash_func('Joe') & (capacity - 1);
 */
typedef size_t (*hash_func) (const_keyT);


/**
 * @typedef keyT_func
 * A function that receives a const_keyT,
 * and returns 1 if it fulfills some condition, and 0 else
 */
typedef int (*keyT_func) (const_keyT);

/**
 * @typedef valueT_func
 * A function that changes the value of a valueT, in-place
 */
typedef void (*valueT_func) (valueT);

/**
 * @struct hashmap
 * @param buckets dynamic array of vectors which stores the values.
 * @param size the number of elements (pairs) stored in the hash map.
 * @param capacity the number of buckets in the hash map.
 * @param hash_func a function which "hashes" keys.
 */
typedef struct hashmap {
    vector **buckets;
    size_t size;
    size_t capacity; // num of buckets
    hash_func hash_func;
} hashmap;

/**
 * Allocates dynamically new hash map element.
 * @param func a function which "hashes" keys.
 * @return pointer to dynamically allocated hashmap.
 * @if_fail return NULL.
 */
hashmap *hashmap_alloc (hash_func func);

/**
 * Frees a hash map and the elements the hash map itself allocated.
 * @param p_hash_map pointer to dynamically allocated pointer to hash_map.
 */
void hashmap_free (hashmap **p_hash_map);

/**
 * Inserts a new in_pair to the hash map.
 * The function inserts *new*, *copied*, *dynamically allocated* in_pair,
 * NOT the in_pair it receives as a parameter.
 * @param hash_map the hash map to be inserted with new element.
 * @param in_pair a in_pair the hash map would contain.
 * @return returns 1 for successful insertion, 0 otherwise.
 */
int hashmap_insert (hashmap *hash_map, const pair *in_pair);

/**
 * The function returns the value associated with the given key.
 * @param hash_map a hash map.
 * @param key the key to be checked.
 * @return the value associated with key if exists,
 * NULL otherwise (the value itself,
 * not a copy of it).
 */
valueT hashmap_at (const hashmap *hash_map, const_keyT key);

/**
 * The function erases the pair associated with key.
 * @param hash_map a hash map.
 * @param key a key of the pair to be erased.
 * @return 1 if the erasing was done successfully,
 * 0 otherwise. (if key not in map,
 * considered fail).
 */
int hashmap_erase(hashmap *hash_map, const_keyT key);

/**
 * This function returns the load factor of the hash map.
 * @param hash_map a hash map.
 * @return the hash map's load factor, -1 if the function failed.
 */
double hashmap_get_load_factor(const hashmap *hash_map);

/**
 * This function receives a hashmap and 2 functions,
 * the first checks a condition on the keys,
 * and the seconds apply some modification on the values.
 * The function should apply the modification
 * only on the values that are associated with
 * keys that meet the condition.
 * Example: if the hashmap maps char->int,
 * keyT_func checks if the char is a capital letter (A-Z),
 * and val_t_func multiples the number by 2,
 * hashmap_apply_if will change the map:
 * {('C',2),('#',3),('X',5)}, to: {('C',4),('#',3),('X',10)},
 * and the return value will be 2.
 * @param hash_map a hashmap
 * @param keyT_func a function that checks a condition on keyT
 * and return 1 if true, 0 else
 * @param valT_func a function that modifies valueT, in-place
 * @return number of changed values
 */
int hashmap_apply_if (const hashmap *hash_map, keyT_func keyT_func,
                      valueT_func valT_func);

/**
 * this funcs get a num from hash funcs, and return the match index at hashmap
 * @param capacity - the capacity of hashmap
 * @param n - the num returned from hash func
 * @return return the match index at hashmap
 */
size_t get_idx_from_hash (size_t capacity, size_t n);

/**
 * this func does rehashing to the hashmap
 * @param hash_map to rehash
 * @param new_cap the num of vectors
 * @return an array of vectors
 */
vector** rehashing (hashmap *hash_map, size_t new_cap);

/**
 * this func take a pair and add it to
 * @param vec - a vector to add a pair to it
 * @param p - pair
 * @return 1 if we success to add the vec, and 0 else
 */
int add_to_vec(vector** vec, const pair* p);

/**
 * this funcs take an array of vector and free if
 * @param p_vectors - vectors to free
 * @param capacity - num of vectors to free
 */
void free_vectors(vector*** p_vectors, size_t capacity);


hashmap *hashmap_alloc (hash_func func)
{
  if (func == NULL)
    {
      return NULL;
    }
  hashmap* hash_map = (hashmap*) malloc(sizeof(hashmap));
  if (hash_map == NULL)
    {
      return NULL;
    }
  hash_map->capacity = HASH_MAP_INITIAL_CAP;
  hash_map->size = 0;
  hash_map->hash_func = func;
  hash_map->buckets = (vector**)calloc(hash_map->capacity, sizeof(vector*));
  if (hash_map->buckets == NULL)
    {
      hashmap_free(&hash_map); //check

      return NULL;
    }

  return hash_map;

}


void hashmap_free (hashmap **p_hash_map)
{
  for (size_t i = 0; i < (*p_hash_map)->capacity; ++i)
    {
      if ((*p_hash_map)->buckets[i] != NULL)
        {

          vector_free (&((*p_hash_map)->buckets[i]));
        }
    }
  free((*p_hash_map)->buckets);
  free(*p_hash_map);
  *p_hash_map = NULL;
}


int hashmap_insert (hashmap *hash_map, const pair *in_pair)
{
  if (hash_map == NULL || in_pair == NULL || hash_map->capacity == 0 ||
      hash_map->buckets == NULL)
    {
      return 0;
    }
  if (hashmap_at (hash_map, in_pair->key) != NULL) // there is exist a pair of
    // that key
    {
      return 0;
    }
  hash_map->size++;
  if (hashmap_get_load_factor (hash_map) > HASH_MAP_MAX_LOAD_FACTOR)
    // we need to change the capacity
    {
      vector** vectors = rehashing (hash_map, hash_map->capacity *
                                              HASH_MAP_GROWTH_FACTOR);
      if (vectors == NULL)
        {
          hash_map->size--;
          return 0;
        }

      //alloc sucsess
      size_t idx = get_idx_from_hash
          (hash_map->capacity * HASH_MAP_GROWTH_FACTOR,
                                      hash_map->hash_func
                                          (in_pair->key));
      if (add_to_vec (&(vectors[idx]), in_pair) == 0)
        {
          free_vectors(&vectors, hash_map->capacity);
          hash_map->size--;
          return 0;
        }
      else // the addition success
        {
          free_vectors(&(hash_map->buckets), hash_map->capacity);
          hash_map->buckets = vectors;
          hash_map->capacity = hash_map->capacity *
                               HASH_MAP_GROWTH_FACTOR;
        }

    }
  else
    {
      size_t idx2 = get_idx_from_hash (hash_map->capacity, hash_map->hash_func
          (in_pair->key));

      if (add_to_vec ((&hash_map->buckets[idx2]), in_pair) == 0)
        {
          hash_map->size--;
          return 0;
        }

    }

  return 1;
}


valueT hashmap_at (const hashmap *hash_map, const_keyT key)
{
  if (hash_map == NULL || key == NULL)
    {
      return NULL;
    }
  for (size_t i = 0; i < hash_map->capacity; ++i)
    {
      if (hash_map->buckets[i] != NULL)
        {
          for (size_t j = 0; j < hash_map->buckets[i]->size; ++j)
            {
              pair* pair_found = (pair*)vector_at(hash_map->buckets[i],j);
              if (pair_found->key_cmp(pair_found->key, key))
                {
                  return pair_found->value;
                }

            }
        }
    }
  return NULL;
}


int hashmap_erase(hashmap *hash_map, const_keyT key)
{
  if (hash_map == NULL || key == NULL || hashmap_at(hash_map, key) == NULL
      || hash_map->buckets == NULL)
    {
      return 0;
    }
  hash_map->size--;
  if (hashmap_get_load_factor (hash_map) < HASH_MAP_MIN_LOAD_FACTOR)
    {
      double num = ((double) hash_map->capacity / 2);
      size_t new_cap = (int) num;
      vector** vectors = rehashing (hash_map, new_cap);
      if (vectors == NULL)
        {
          hash_map->size++;
          return 0;
        }

      for (size_t i = 0; i < new_cap; ++i)
        {
          if (vectors[i] != NULL)
            {
              for (size_t j = 0; j < vectors[i]->size; ++j)
                {
                  pair *pair_found = (pair *) vector_at
                      (vectors[i], j);
                  if (pair_found->key_cmp(pair_found->key, key))
                    {
                      if (vector_erase(vectors[i], j) == 0)
                        {
                          hash_map->size++;
                          free_vectors(&vectors, new_cap);
                          return 0;
                        }
                      // on success
                      free_vectors(&(hash_map->buckets), hash_map->capacity);
                      hash_map->buckets = vectors;
                      hash_map->capacity = new_cap;
                      return 1;
                    }
                }

            }
        }
    }

  else
    {
      for (size_t i = 0; i < hash_map->capacity; ++i)
        {
          if (hash_map->buckets[i] != NULL)
            {
              for (size_t j = 0; j < hash_map->buckets[i]->size; ++j)
                {
                  pair *pair_found = (pair *)
                      vector_at (hash_map->buckets[i], j);
                  if (pair_found->key_cmp (pair_found->key, key))
                    {
                      if (vector_erase (hash_map->buckets[i], j) == 0)
                        {
                          hash_map->size++;
                          return 0;
                        }
                      return 1;
                    }
                }
            }
        }
    }

  return 1;
}


double hashmap_get_load_factor(const hashmap *hash_map)
{
  if (hash_map == NULL)
    {
      return -1;
    }
  if (hash_map->capacity == 0)
    {
      return -1;
    }
  return ((double) hash_map->size / hash_map->capacity);

}


int hashmap_apply_if (const hashmap *hash_map, keyT_func keyT_func,
                      valueT_func valT_func)//const
{
  if (keyT_func == NULL || valT_func == NULL || hash_map == NULL)
    {
      return -1;
    }
  int num_of_changes = 0;
  for (size_t i = 0; i < hash_map->capacity; ++i)
    {
      if (hash_map->buckets[i] != NULL)
        {
          for (size_t j = 0; j < hash_map->buckets[i]->size; ++j)
            {
              if (keyT_func(((pair*)(hash_map->buckets[i]->data[j]))->key))
                {
                  valT_func(((pair*)(hash_map->buckets[i]->data[j]))->value);
                  num_of_changes++;


                }
            }
        }
    }
  return num_of_changes;

}




size_t get_idx_from_hash (size_t capacity, size_t n)
{
  return (n & (capacity - 1));
}

vector** rehashing (hashmap *hash_map, size_t new_cap)
{
  vector** vectors = (vector**)calloc(new_cap, sizeof(vector*));
  if (vectors == NULL)
    {
      return NULL;
    }

  for (size_t i = 0; i < hash_map->capacity; ++i)
    {
      if (hash_map->buckets[i] != NULL)
        {
          for (size_t j = 0; j < hash_map->buckets[i]->size; ++j)
            {
              size_t idx = get_idx_from_hash (new_cap, hash_map->hash_func
                  (((pair*)((hash_map->buckets[i])->data[j]))->key));

              if (add_to_vec(&(vectors[idx]), ((hash_map->buckets[i])
                  ->data[j]))
                  //the insertion not success
                  == 0)
                {
                  free_vectors(&vectors, new_cap);
                  return NULL;
                }
            }
        }
    }

  return vectors;
}

int add_to_vec(vector** vec, const pair* p)
{
  if (vec == NULL || p == NULL)
    {
      return 0;
    }

  if (*vec == NULL) //  initialize a vector
    {
      *vec = vector_alloc (pair_copy, pair_cmp,
                           pair_free);
      if (*vec == NULL)
        {
          return 0;
        }

      if (vector_push_back(*vec, p) == 0)
        {
          vector_free(&(*vec));
          return 0;
        }
      return 1;

    }

  else if (vector_push_back(*vec, p) == 0)
    {
      return 0;
    }

  return 1;

}

void free_vectors(vector*** p_vectors, size_t capacity)
{
  for (size_t i = 0; i < capacity; ++i)
    {
      vector_free(&((*p_vectors)[i]));
    }
  free(*p_vectors);

  *p_vectors = NULL;

}


#endif //HASHMAP_H_