package src.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.collisions.GameObjectCollection;
import danogl.gui.UserInputListener;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

/**
 * this class represent the mock paddle
 */
public class MockPaddle extends Paddle {

    public static boolean 	isInstantiated = false;
    private final int numCollisionsToDisappear;
    private final GameObjectCollection gameObjectCollection;
    private int count = 0;

    /**
     * Construct a new GameObject instance.
     * @param topLeftCorner - Position of the object, in window coordinates
     * @param dimensions - Width and height in window coordinates.
     * @param renderable -The renderable representing the object. Can be null, in which case
     * @param inputListener - listener object for user input.
     * @param windowDimensions - dimensions of game window.
     * @param gameObjectCollection - collections of game objects
     * @param minDistanceFromEdge border for paddle movement.
     * @param numCollisionsToDisappear - num collosions needed that the bock paddle disappear
     */
    public MockPaddle(danogl.util.Vector2 topLeftCorner,
                      danogl.util.Vector2 dimensions,
                      danogl.gui.rendering.Renderable renderable,
                      danogl.gui.UserInputListener inputListener,
                      danogl.util.Vector2 windowDimensions,
                      danogl.collisions.GameObjectCollection gameObjectCollection,
                      int minDistanceFromEdge,
                      int numCollisionsToDisappear){
        super(topLeftCorner, dimensions, renderable, inputListener, windowDimensions, minDistanceFromEdge);
        isInstantiated = true;
        this.numCollisionsToDisappear = numCollisionsToDisappear;
        this.gameObjectCollection = gameObjectCollection;
    }

    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        count++;
        if (count == numCollisionsToDisappear){
            gameObjectCollection.removeGameObject(this);
        }
    }
}
