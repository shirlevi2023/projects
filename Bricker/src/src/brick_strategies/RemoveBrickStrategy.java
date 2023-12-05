package src.brick_strategies;
import danogl.GameObject;
import danogl.collisions.GameObjectCollection;
import danogl.collisions.Layer;
import danogl.util.Counter;

/**
 * Says what to do when brick collided with ball.
 */
public class RemoveBrickStrategy implements CollisionStrategy {
    private final GameObjectCollection gameObjects;

    /**
     * construcor of  class CollisionStrategy
     * @param gameObjects - a collection of game objects
     */
    public RemoveBrickStrategy(GameObjectCollection gameObjects) {
        this.gameObjects = gameObjects;
    }

    /**
     * a getter return game object collection
     */
    public GameObjectCollection getGameObjectCollection(){
        return gameObjects;
    }

    /**
     * To be called on brick collision.
     * @param thisObj - the current obj that has collision
     * @param otherObj - the other obj that collide with the current obj
     * @param counter -  global brick counter.
     */
    public void onCollision(GameObject thisObj, GameObject otherObj, Counter counter) {
        boolean isRemoved = gameObjects.removeGameObject(thisObj, Layer.STATIC_OBJECTS);
        if (isRemoved){
            counter.increaseBy(-1);
        }


    }

}
