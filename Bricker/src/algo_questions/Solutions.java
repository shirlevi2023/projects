package algo_questions;

import java.util.Arrays;

import static java.lang.Math.max;


public class Solutions {

    /**
     * Method computing the maximal amount of tasks out of n tasks that can be
     * completed with m time slots.
     * @param tasks- the tasks to divide to time slots
     * @param timeSlots - an array of times to insert tasks
     * @return the max num of tasks that can divide to times slots
     */
    public static int alotStudyTime(int[] tasks, int[] timeSlots){
        Arrays.sort(timeSlots);
        Arrays.sort(tasks);
        int tasksIdx = 0;
        int timeSlotsIdx = 0;
        int countTasksPossible = 0;
        while (timeSlotsIdx < timeSlots.length && tasksIdx < tasks.length){
            if (tasks[tasksIdx] <= timeSlots[timeSlotsIdx]) { // check if possible to insert the task
                // to time slot
                countTasksPossible++;
                tasksIdx++;
            }
            timeSlotsIdx++;
        }
        return countTasksPossible;
    }

    /**
     * Method computing the nim amount of leaps a frog needs to jump across n waterlily
     * leaves, from leaf 1 to leaf n.
     * @param leapNum - an array of numbers on each leap
     * @return minimal jumps to arrive thhe end leap
     */
    public static int minLeap(int[] leapNum){
        if(leapNum.length <= 1){
            return 0;
        }
        int jumps = 0;
        int idxVal = 0;
        int maxReach = 0;
        for(int k = 0; k < leapNum.length - 1; k++){
            maxReach = max(maxReach, k + leapNum[k]);
            if(leapNum.length + 1 <= maxReach){
                if (jumps == 0){ // if we can arrive to the end point from the
                    // first point
                    jumps = 1;
                }
                return jumps;
            }
            if (idxVal == k){ //when we arrive here and we find a better point from the
                // current, we update the idx val
                jumps++;
                idxVal = maxReach;
                maxReach = 0;
            }
        }
        return jumps;
    }

    /**
     Method computing the solution to the following problem:
     A boy is filling the water trough for his father's cows in their village.
     The trough holds n liters of water. With every trip to the village well,
     he can return using either the 2 bucket yoke, or simply with a single bucket. A bucket holds 1 liter.
     In how many different ways can he fill the water trough? n can be assumed to be
     greater or equal to 0, less than or equal to 48.
     * @param n - liters that can fill the well
     * @return num of ways to fill the well
     */
    public static int bucketWalk(int n){
        // base cases
        if(n == 0){
            return 1;
        }

        if (n == 1){
            return 1;
        }
        int[] waysToFillTheWell = new int[n + 1]; // the solution here
        waysToFillTheWell[0] = waysToFillTheWell[1] = 1;

        for(int j = 2; j < n + 1; j++){
            waysToFillTheWell[j] = waysToFillTheWell[j - 2] + waysToFillTheWell[j - 1];
        }
        return waysToFillTheWell[n];
    }

    /**
     * Method computing the solution to the following problem:
     * Given an integer n, return the number of structurally unique BST's (binary search trees)
     * which has exactly n nodes of unique values from 1 to n. You can assume n is at least 1 and at most 19. (Definition: two trees S and T are structurally distinct if one can not be obtained from the other by renaming of the nodes
     * @param n - num of nodes
     * @returnnum of possible unique trees for n nodes
     */
    public static int numTrees(int n){
        // base cases
        if(n == 0){
            return 0;
        }
        if(n == 1){
            return 1;
        }
        int[] numTreesUntilN = new int[n + 1];
        numTreesUntilN[0] = 1;
        numTreesUntilN[1] = 1;
        for(int i = 2; i <= n; i++){
            for(int j = 1; j <= i; j++){
                numTreesUntilN[i] += numTreesUntilN[j - 1] * numTreesUntilN[i - j];
            }
        }
        return numTreesUntilN[n];
    }


}
