#ifndef TESTSUITE_H_
#define TESTSUITE_H_


#include <assert.h>
#include <stdlib.h>

#include "test_suite.h"
#include "test_pairs.h"
#include "hash_funcs.h"
#include "hashmap.h"

pair* create_pair(const_keyT key, const_valueT value);


void test_invalid_inputs_and_simple_insert(void);
void test_rehashing_up(void);
void test_invalid_inputs_and_simple_erase(void);
void test_rehashing_down(void);
void basic_load_factor_tests(void);
void rehashing_load_factor_tests(void);
pair* create_pair_of_int_and_char(const_keyT key, const_valueT value);

/**
 * This function checks the hashmap_insert
 * function of the hashmap library.
 * If hashmap_insert fails at some points,
 * the functions exits with exit code 1.
 */
void test_hash_map_insert(void)
{
  test_invalid_inputs_and_simple_insert();
  test_rehashing_up();
}

/**
 * This function checks the hashmap_at function of the hashmap library.
 * If hashmap_at fails at some points, the functions exits with exit code 1.
 */
void test_hash_map_at(void)
{
  pair *pairs[14];
  int arr1[14] = {0,2,4,6,8,10,12,14,16,18,20,22,24,26};
  int arr2[14] = {1,3,5,7,9,11,13,15,17,19,21,23,25,27};

  for (int j = 0; j < 14; ++j)
    {
      int key = arr1[j];
      int value = arr2[j];

      pairs[j] = pair_alloc (&key, &value, int_value_cpy, int_value_cpy,
                             int_value_cmp,
                             int_value_cmp, int_value_free, int_value_free);
    }
  // Create hash-map and inserts elements into it, using pair_char_int.h
  hashmap *map = hashmap_alloc (hash_int);
  for (int p = 0; p < 13; ++p)
    {
      hashmap_insert(map, pairs[p]);
    }

    // invalid inputs
  assert(hashmap_at(NULL, pairs[0]->key) == NULL);
  assert(hashmap_at(map, NULL) == NULL);

  //key valid but not at map
  assert(hashmap_at(NULL, pairs[13]->key) == NULL);
  int k = 27;
  int v = 26;
  pair* new_pair = pair_alloc (&k, &v, int_value_cpy, int_value_cpy,
                               int_value_cmp,
                               int_value_cmp, int_value_free, int_value_free);
  // if the key that we search appears as a value
  hashmap_insert(map, new_pair);
  assert(hashmap_at(NULL, pairs[13]->key) == NULL);

  assert(*((int*)(hashmap_at(map, pairs[2]->key))) == 5);
  hashmap_free(&map);
  for (int p = 0; p < 14; ++p)
    {
      pair_free((void **)&pairs[p]);
    }

  pair_free((void **)&new_pair);

}




/**
 * This function checks the hashmap_erase function of the hashmap library.
 * If hashmap_erase fails at some points, the functions exits with exit code 1.
 */
void test_hash_map_erase(void)
{
  test_invalid_inputs_and_simple_erase();
  test_rehashing_down();

}

/**
 * This function checks the hashmap_get_load_factor
 * function of the hashmap library.
 * If hashmap_get_load_factor fails at some points,
 * the functions exits with exit code 1.
 */
void test_hash_map_get_load_factor(void)
{
  basic_load_factor_tests();
  rehashing_load_factor_tests();
}

/**
 * This function checks the HashMapGetApplyIf
 * function of the hashmap library.
 * If HashMapGetApplyIf fails at some points,
 * the functions exits with exit code 1.
 */
void test_hash_map_apply_if()
{
  hashmap *map = hashmap_alloc (hash_char);
  char key = 'a';
  int value = 0;

  for (int j = 0; j < 5; ++j)
    {
      if (j % 2 == 0)
        {
          key = (char)j + '0';
        }
      else
        {
          key = 'a' + j;
         }
      value = j;
      pair *p = create_pair_of_int_and_char(&key, &value);
      hashmap_insert(map, p);
      pair_free((void **)&p);
    }

    // checks invalid inputs
  assert(hashmap_apply_if(NULL, is_digit, double_value) == -1);
  assert(hashmap_apply_if(map, NULL, double_value) == -1);
  assert(hashmap_apply_if(map, is_digit, NULL) == -1);


  // checks the func changes according to the funcs
  hashmap_apply_if(map, is_digit, double_value);
  assert(*(int*)(((pair*)(map->buckets[0]->data[0]))->value) == 0);
  assert(*(int*)(((pair*)(map->buckets[2]->data[0]))->value) == 1);
  assert(*(int*)(((pair*)(map->buckets[2]->data[1]))->value) == 4);
  assert(*(int*)(((pair*)(map->buckets[4]->data[0]))->value) == 3);
  assert(*(int*)(((pair*)(map->buckets[4]->data[1]))->value) == 8);
  assert(hashmap_apply_if(map, is_digit, double_value) == 3);

  hashmap_free(&map);

}

/**
 * this funcs test invalid inputs and a simple insertion
 */
void test_invalid_inputs_and_simple_insert()
{
  hashmap *hashmap1 = hashmap_alloc (hash_int);
  int key = 1;
  int value = 0;
  pair* pair1 = create_pair(&key, &value);

  //checking validity of input
  assert(hashmap_insert(NULL, pair1) == 0);
  assert(hashmap_insert(hashmap1, NULL) == 0);

  hashmap_insert(hashmap1, pair1);

  //insert an key that already exist
 //when the pair is equal to the prev
  pair* pair2 = create_pair(&key, &value);
  assert(hashmap_insert(hashmap1, pair2) == 0);

  int v1 = 2; //when the key is equal to prev but val not
  pair* pair3 = create_pair(&key, &v1);
  assert(hashmap_insert(hashmap1, pair3) == 0);
  assert(hashmap1->size == 1);
  assert(hashmap1->capacity == HASH_MAP_INITIAL_CAP);

  hashmap_free(&hashmap1);
  pair_free((void *)&pair1);
  pair_free((void *)&pair2);
  pair_free((void *)&pair3);

}

/**
 * this funcs test the reshashing up at insertion
 */
void test_rehashing_up()
{
  pair *pairs[14];
  int arr1[14] = {0,2,4,6,8,10,12,14,16,18,20,22,24,26};
  int arr2[14] = {1,3,5,7,9,11,13,15,17,19,21,23,25,27};

  for (int j = 0; j < 14; ++j)
    {
      int key = arr1[j];
      int value = arr2[j];

      pairs[j] = pair_alloc (&key, &value, int_value_cpy, int_value_cpy,
                             int_value_cmp,
                             int_value_cmp, int_value_free, int_value_free);
    }
  // Create hash-map and inserts elements into it
  hashmap *map = hashmap_alloc (hash_int);
  for (size_t p = 0; p < 14; ++p)
    {
      hashmap_insert(map, pairs[p]);
      assert(map->size == p+1);

    }
  assert(map->capacity == HASH_MAP_INITIAL_CAP * 2);

  hashmap_free(&map);
  for (int p = 0; p < 14; ++p)
    {
      pair_free((void **)&pairs[p]);
    }
}

/**
 * this func test invalid inputs and simple erasing
 */
void test_invalid_inputs_and_simple_erase()
{
  hashmap *hashmap1 = hashmap_alloc (hash_int);
  int key = 1;
  int value = 0;
  pair* pair1 = create_pair(&key, &value);

  //checking validity of input
  assert(hashmap_erase(NULL, pair1->key) == 0);
  assert(hashmap_erase(hashmap1, NULL) == 0);
  assert(hashmap_erase(hashmap1, pair1->key) == 0);
  assert(hashmap1->size == 0);

  //free all
  pair_free((void **)&pair1);
  hashmap_free(&hashmap1);
}

/**
 * this funcs test the reshasing down at deletion
 */
void test_rehashing_down()
{
  pair *pairs[5];
  int arr1[5] = {0,2,4,6,8};
  int arr2[5] = {1,3,5,7,9};

  for (int j = 0; j < 5; ++j)
    {
      int key = arr1[j];
      int value = arr2[j];

      pairs[j] = pair_alloc (&key, &value, int_value_cpy, int_value_cpy,
                             int_value_cmp,
                             int_value_cmp, int_value_free, int_value_free);
    }
  // Create hash-map and inserts elements into it
  hashmap *map = hashmap_alloc (hash_int);
  for (size_t p = 0; p < 5; ++p)
    {
      hashmap_insert(map, pairs[p]);
    }

  for (size_t p = 0; p < 5; ++p)
    {
      hashmap_erase(map, pairs[p]->key);
      assert(map->size == 5 - p - 1);
    }

  assert(map->capacity == 2);
  hashmap_free(&map);
  for (int p = 0; p < 5; ++p)
    {
      pair_free((void **)&pairs[p]);
    }

}
/**
 * this func tests basic of the load factor
 */
void basic_load_factor_tests()
{
  assert(hashmap_get_load_factor(NULL) == -1);
  pair *pairs[5];
  int arr1[5] = {0,2,4,6,8};
  int arr2[5] = {1,3,5,7,9};

  for (int j = 0; j < 5; ++j)
    {
      int key = arr1[j];
      int value = arr2[j];

      pairs[j] = pair_alloc (&key, &value, int_value_cpy, int_value_cpy,
                             int_value_cmp,
                             int_value_cmp, int_value_free, int_value_free);
    }
  // Create hash-map and inserts elements into it, using pair_char_int.h
  hashmap *map = hashmap_alloc (hash_int);
  assert(hashmap_get_load_factor(map) == 0.0);
  for (size_t p = 0; p < 5; ++p)
    {
      hashmap_insert(map, pairs[p]);
      assert(hashmap_get_load_factor(map) == (((double )(map->size)) /
                                              map->capacity));

    }

  hashmap_free(&map);
  for (int p = 0; p < 5; ++p)
    {
      pair_free((void **)&pairs[p]);
    }
}

/**
 * this func test load factor when we do rehash
 */
void rehashing_load_factor_tests(void)
{
  pair *pairs[14];
  int arr1[14] = {0,2,4,6,8,10,12,14,16,18,20,22,24,26};
  int arr2[14] = {1,3,5,7,9,11,13,15,17,19,21,23,25,27};

  for (int j = 0; j < 14; ++j)
    {
      int key = arr1[j];
      int value = arr2[j];

      pairs[j] = pair_alloc (&key, &value, int_value_cpy, int_value_cpy,
                             int_value_cmp,
                             int_value_cmp, int_value_free, int_value_free);
    }
  // Create hash-map and inserts elements into it, using pair_char_int.h
  hashmap *map = hashmap_alloc (hash_int);
  for (int p = 0; p < 14; ++p)
    {
      hashmap_insert(map, pairs[p]);
    }
  assert(hashmap_get_load_factor(map) == ((double )14 / 32));

  int s = 0;
  while (s != 27)
    {
      if (s % 2 == 0)
        {
          hashmap_erase (map, &s);
          s++;
          continue;

        }
      s++;
    }

  assert(hashmap_get_load_factor(map) == 0.0);
  assert(map->capacity == HASH_MAP_GROWTH_FACTOR);
  hashmap_free(&map);
  for (int p = 0; p < 14; ++p)
    {
      pair_free((void **)&pairs[p]);
    }

}

#endif //TESTSUITE_H_
