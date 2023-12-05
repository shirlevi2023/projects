package src.brick_strategies;

import danogl.GameObject;
import danogl.collisions.GameObjectCollection;
import danogl.util.Counter;
import src.brick_strategies.CollisionStrategy;

public abstract class RemoveBrickStrategyDecorator implements CollisionStrategy {
    private final CollisionStrategy toBeDecorated;

    /**
     * a constructor to remove brick strategy decorator class
     * @param toBeDecorated - collision strategy to decorated
     */
    RemoveBrickStrategyDecorator(CollisionStrategy toBeDecorated){
        this.toBeDecorated = toBeDecorated;
    }

    @Override
    public void onCollision(GameObject thisObj, GameObject otherObj, Counter counter) {
        toBeDecorated.onCollision(thisObj, otherObj, counter);
    }

    /**
     * a getter return game object collection
     */
    public GameObjectCollection getGameObjectCollection(){
        return toBeDecorated.getGameObjectCollection();

    }
}
