package src.brick_strategies;

import danogl.GameObject;
import danogl.collisions.GameObjectCollection;

/**
 * General type for brick strategies,
 * part of decorator pattern implementation. All brick strategies implement this interface.
 */
public interface CollisionStrategy {

    /**
     * to be called on a brick collision
     * @param thisObj the brick
     * @param otherObj - other obj that collide with the brick
     * @param counter - manage counter for the num of bricks
     */
    void onCollision(GameObject thisObj, GameObject otherObj,
                            danogl.util.Counter counter);

    /**
     * a getter return game object collection
     */
    GameObjectCollection getGameObjectCollection();
}







