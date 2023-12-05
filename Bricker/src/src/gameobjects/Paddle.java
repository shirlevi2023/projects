package src.gameobjects;

import danogl.GameObject;
import danogl.gui.UserInputListener;
import danogl.util.Vector2;

import java.awt.event.KeyEvent;

public class Paddle extends GameObject {
    private static final float MOVEMENT_SPEED = 300;
    private final float windowWidth;
    private final int minDistanceFromEdge;
    private final UserInputListener inputListener;

    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     * @param minDistanceFromEdge - border for paddle movement
     */
    public Paddle(danogl.util.Vector2 topLeftCorner,
                  danogl.util.Vector2 dimensions,
                  danogl.gui.rendering.Renderable renderable,
                  danogl.gui.UserInputListener inputListener,
                  danogl.util.Vector2 windowDimensions,
                  int minDistanceFromEdge) {
        super(topLeftCorner, dimensions, renderable);
        this.inputListener = inputListener;
        this.windowWidth = windowDimensions.x();
        this.minDistanceFromEdge = minDistanceFromEdge;
    }

    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);
        Vector2 movementDir = Vector2.ZERO;
        if (inputListener.isKeyPressed(KeyEvent.VK_LEFT)){
            movementDir = movementDir.add(Vector2.LEFT);
        }
        if (inputListener.isKeyPressed(KeyEvent.VK_RIGHT)){
            movementDir = movementDir.add(Vector2.RIGHT);
        }
        setVelocity(movementDir.mult(MOVEMENT_SPEED));
//        transform().setTopLeftCornerX(50);
        float TopLeftCorner = getTopLeftCorner().x();


        if (TopLeftCorner <= minDistanceFromEdge){
            this.setTopLeftCorner(new Vector2(minDistanceFromEdge,
                    this.getTopLeftCorner().y()));
        }
        if(TopLeftCorner > windowWidth - minDistanceFromEdge - getDimensions().x()){
            this.setTopLeftCorner(new Vector2(
                    windowWidth - minDistanceFromEdge - getDimensions().x()
                    , this.getTopLeftCorner().y()));

        }


//        if ( (TopLeftCorner < minDistanceFromEdge) || (TopLeftCorner > windowWidth - minDistanceFromEdge - getDimensions().x())){
//            if (TopLeftCorner  < minDistanceFromEdge){
//                transform().setTopLeftCornerX(minDistanceFromEdge);
//            }
//            else {
//                transform().setTopLeftCornerX(windowWidth - minDistanceFromEdge - getDimensions().x());
//            }
//
//        }


    }
}


//        if ( (TopLeftCorner + 1  > 20) || (TopLeftCorner > windowWidth - minDistanceFromEdge - getDimensions().x())){
//                if (TopLeftCorner + 1  > 20){
////                System.out.println("yes");
//                if (TopLeftCorner - 1 < 20){
//        transform().setTopLeftCornerX(30);
//        }
//        }
//        else {
//        transform().setTopLeftCornerX(windowWidth - minDistanceFromEdge - getDimensions().x());
//        }
//
//        }