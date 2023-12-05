package src.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.collisions.GameObjectCollection;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

public class ExtendContract extends StatusDefiner {
    private static final int FACTOR_OF_EXTEND = 25;
    private final boolean res;


    /**
     * Construct a new GameObject instance.
     *  @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     * @param center - a center of the brick
     * @param res - a boolean parameter means the img chose
     */
    public ExtendContract(Vector2 topLeftCorner, Vector2 dimensions,
                          Renderable renderable, Vector2 center, boolean res, GameObjectCollection gameObjects){
        super(topLeftCorner, dimensions, renderable, center, res, gameObjects);
        this.res = res;
    }

    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        if (other instanceof Paddle){
            if (res){
                other.setDimensions(new Vector2(other.getDimensions().x()+ FACTOR_OF_EXTEND
                        , other.getDimensions().y()));
            }
            else {
                other.setDimensions(new Vector2((other.getDimensions().x()-FACTOR_OF_EXTEND)
                        , other.getDimensions().y()));
            }
        }

    }

}
