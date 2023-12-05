package src.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.gui.Sound;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

/**
 * Ball is the main game object.
 */
public class Ball extends GameObject {
    private final Sound collisionSound;
    private int count;

//    private static final float BALL_DIM = 20;

    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     */
    public Ball(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable,
                Sound collisionSound) {
        super(topLeftCorner, dimensions, renderable);
        this.collisionSound = collisionSound;
        this.count = 0;
    }

    /**
     * On collision, object velocity is reflected about the normal
     * vector of the surface it collides with.
     * @param other
     * @param collision
     */
    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        count ++;
        setVelocity(getVelocity().flipped(collision.getNormal()));
        collisionSound.play();

    }

    int getCollisionCount(){
        return count;
    }
}
