package src.gameobjects;

import src.brick_strategies.CollisionStrategy;
import src.brick_strategies.CollisionStrategy;
import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.gui.rendering.Renderable;
import danogl.util.Counter;
import danogl.util.Vector2;
//import src.brick_strategies.CollisionStrategy;

public class Brick extends GameObject {

    private final Counter counter;
    private final CollisionStrategy collisionStrategy;
//    private boolean isFirstCollision = true;

    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     */
    public Brick(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable,
                 CollisionStrategy collisionStrategy, Counter counter) {
        super(topLeftCorner, dimensions, renderable);
        this.collisionStrategy = collisionStrategy;
        this.counter = counter;
    }

    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        if (collisionStrategy == null){
            return;
        }
        if (other instanceof  Ball){
            collisionStrategy.onCollision(this, other, counter);
        }

    }
}
