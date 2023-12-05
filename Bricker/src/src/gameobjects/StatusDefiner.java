package src.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.collisions.GameObjectCollection;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

public  class StatusDefiner extends GameObject {
    private final GameObjectCollection gameObjects;
    private final boolean res;

    @Override
    public boolean shouldCollideWith(GameObject other) {
        return other instanceof Paddle;
    }

    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);

    }

    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        if (other instanceof  Paddle){

            gameObjects.removeGameObject(this);
        }

//        if (other instanceof Paddle){
//            if (res){
//                other.setDimensions(new Vector2(other.getDimensions().x()* 2
//                        , other.getDimensions().y()));
//            }
//            else {
//                other.setDimensions(new Vector2((other.getDimensions().x()/2)
//                        , other.getDimensions().y()));
//            }
//        }

    }

    /**
     * Construct a new GameObject instance.
     *  @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     * @param center - center of a brick
     */
    public StatusDefiner(Vector2 topLeftCorner, Vector2 dimensions,
                         Renderable renderable,
                         Vector2 center, boolean res, GameObjectCollection gameObjects) {
        super(topLeftCorner, dimensions, renderable);
        this.gameObjects = gameObjects;
        this.res = res;



    }
}
