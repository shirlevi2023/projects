package src;

import src.brick_strategies.BrickStrategyFactory;
import src.brick_strategies.CollisionStrategy;
import danogl.GameManager;
import danogl.GameObject;

import danogl.collisions.Layer;
import danogl.components.CoordinateSpace;
import danogl.gui.*;
import danogl.gui.rendering.Renderable;
import danogl.util.Counter;
import danogl.util.Vector2;
import src.gameobjects.*;

import java.util.Random;

public class BrickerGameManager extends GameManager {
    private static final float BORDER_WIDTH = 20;
    private static final float BALL_SPEED = 200;
    private static final int BRICKS_PER_ROW = 5; //5
    private static final int BRICKS_PER_COL = 8; //8
    private static final int minDistanceFromEdge = 10;
    private static final String WINDOW_TITLE = "Bricker";
    private static final String BALL_IMAGE_PATH = "assets/ball.png";
    private static final String COLLISION_SOUND_PATH = "assets/blop_cut_silenced.wav";
    private static final float BALL_DIM = 20;
    private static final String PADDLE_PATH = "assets/paddle.png";
    private static final float WINDOW_REDUCTION_FACTOR = 0.5f;
    private static final float PADDLE_SIZE_X = 100;
    private static final float PADDLE_SIZE_Y = 15;
    private static final int NUM_OF_LIVES = 4;
    private static final String LOSE_MSG = "You lose!";
    private static final String WIN_MSG = "You win!";
    private static final String PLAY_AGAIN_MSG = " play again?";
    private static final String BRICK_PATH = "assets/brick.png";
    private static final String BACKROUND_PATH = "assets/DARK_BG2_small.jpeg";
    private static final String HEARK_IMAGE_PATH = "assets/heart.png";
    private static final int TARGET_FRAMERATE = 80;
    private static final float WINDOE_SIZE_X = 700;
    private static final float WINDOE_SIZE_Y = 500;

    private GameObject ball;
    private Vector2 windowDimensions;
    private WindowController windowController;
//    private GameObjectCollection livesObjects;
    private Counter counterLives;
    private Counter counterBricks;


    @Override
    public void initializeGame(ImageReader imageReader, SoundReader soundReader, UserInputListener inputListener, WindowController windowController) {
        windowController.setTargetFramerate(TARGET_FRAMERATE);
        super.initializeGame(imageReader, soundReader, inputListener, windowController);
        this.windowController = windowController;
        windowController.setTimeScale(0.9f);

        // create Ball
        creatingBall(imageReader, soundReader, windowController);
        // create paddle
        creatingPaddle(imageReader, inputListener);
        addingWallsToGame(windowDimensions);

        // create background

        creatingBackround(imageReader, windowController);


        // create factory
        BrickStrategyFactory bricksFactory =
                new BrickStrategyFactory(this.gameObjects(), this, imageReader,
                        soundReader, inputListener, windowController, windowDimensions);


        // create bricks
        counterBricks = new Counter(0);
        creatingBricks(windowDimensions.x(), imageReader, counterBricks, bricksFactory);

        // create graphic counter
        creatingGraphicCounter(imageReader);

        // create numeric counter
        creatingNumericCounter();

    }



    private void creatingBall(ImageReader imageReader, SoundReader soundReader, WindowController windowController) {
        Renderable ballImage = imageReader.readImage(BALL_IMAGE_PATH, true);
        Sound collisionSound = soundReader.readSound(COLLISION_SOUND_PATH);
        GameObject ball = new Ball(Vector2.ZERO, new Vector2(BALL_DIM, BALL_DIM), ballImage,
                collisionSound);

        float ballVelX = BALL_SPEED;
        float ballVelY = BALL_SPEED;
        Random rand = new Random();
        if (rand.nextBoolean()) {
            ballVelX *= -1;
        }
        if (rand.nextBoolean()) {
            ballVelY *= -1;
        }

        ball.setVelocity(new Vector2(ballVelX, ballVelY));
        this.windowDimensions = windowController.getWindowDimensions();
        ball.setCenter(windowController.getWindowDimensions().mult(WINDOW_REDUCTION_FACTOR));
        this.ball = ball;
        this.gameObjects().addGameObject(ball);
    }

    /**
     * this func create numeric counter
     */
    private void creatingNumericCounter() {
        GameObject numericLifeCounter = new NumericLifeCounter(counterLives,
                new Vector2(0,windowDimensions.y() -100 ), new Vector2(30,30),
                gameObjects());
        this.gameObjects().addGameObject(numericLifeCounter,Layer.BACKGROUND);
    }

    /**
     * this func create graphic counter
     */
    private void creatingGraphicCounter(ImageReader imageReader) {
        this.counterLives = new Counter(NUM_OF_LIVES);
        Renderable levImage = imageReader.readImage(HEARK_IMAGE_PATH,
                true);

        GraphicLifeCounter graphicLifeCounter =
                new GraphicLifeCounter(new Vector2(0,windowDimensions.y()-40),
                        new Vector2(40,40), counterLives,
                        levImage, gameObjects(), NUM_OF_LIVES );

        this.gameObjects().addGameObject(graphicLifeCounter, Layer.BACKGROUND);
    }

    /**
     * this func create the backround of the game
     */
    private void creatingBackround(ImageReader imageReader, WindowController windowController) {
        GameObject background = new GameObject(
                Vector2.ZERO,
                windowController.getWindowDimensions(),
                imageReader.readImage(BACKROUND_PATH, false));

        background.setCoordinateSpace(CoordinateSpace.CAMERA_COORDINATES);
        gameObjects().addGameObject(background, Layer.BACKGROUND);
    }

    /**
     * this func create a paddle
     */
    private void creatingPaddle(ImageReader imageReader, UserInputListener inputListener) {
        Renderable paddleImage = imageReader.readImage(PADDLE_PATH, true);
        GameObject paddle = new Paddle(Vector2.ZERO, new Vector2(PADDLE_SIZE_X,
                PADDLE_SIZE_Y),
                paddleImage, inputListener, windowDimensions, minDistanceFromEdge);
        paddle.setCenter(new Vector2(windowDimensions.x()/2, windowDimensions.y() - 30));
        this.gameObjects().addGameObject(paddle);


//        addingWallsToGame(windowDimensions);
    }

    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);
        float ballHeight = ball.getCenter().y();
        String prompt;
        if (ballHeight > windowDimensions.y()) { // we lost
            counterLives.increaseBy(-1);
            if (counterLives.value() == 0){
                prompt = LOSE_MSG;
                prompt+= PLAY_AGAIN_MSG;
                if (windowController.openYesNoDialog(prompt)){
                    windowController.resetGame();
                }
                else {
                    windowController.closeWindow();
                }
            }
            else {
                ball.setCenter(windowDimensions.mult(WINDOW_REDUCTION_FACTOR));
            }

        }

        if (counterBricks.value() == 0) {
            prompt = WIN_MSG;

            prompt+= PLAY_AGAIN_MSG;
            if (windowController.openYesNoDialog(prompt)){
                windowController.resetGame();
            }
            else {
                windowController.closeWindow();
            }

        }

        for (GameObject obj: this.gameObjects()) {
            if (obj != ball && (obj.getCenter().y() > windowDimensions.y() )){
                this.gameObjects().removeGameObject(obj);
            }

        }

    }
    private void creatingBricks(float windowWidth, ImageReader imageReader, Counter counter, BrickStrategyFactory bricksFactory) {
        float startX = BORDER_WIDTH + 1;
        float startY = BORDER_WIDTH + 1;
        float brickWidth =
                (windowWidth - (BORDER_WIDTH * 2) - BRICKS_PER_COL -1  ) / BRICKS_PER_COL;
        Renderable brickImage = imageReader.readImage(BRICK_PATH, false);
        for (int i = 0; i < BRICKS_PER_ROW; i++) {
            for (int j = 0; j < BRICKS_PER_COL; j++) {
                CollisionStrategy collisionStrategy = bricksFactory.getStrategy();
                gameObjects().addGameObject(new Brick(new Vector2(startX, startY) ,
                        new Vector2(brickWidth, 15), brickImage, collisionStrategy,
                                counter),
                        Layer.STATIC_OBJECTS);
                startX += brickWidth + 1;
                counter.increaseBy(1);
            }
            startY += BORDER_WIDTH + 8 ;
            startX = BORDER_WIDTH + 1;

        }
    }

    private void addingWallsToGame(Vector2 windowDimensions) {
            gameObjects().addGameObject(
                    new GameObject(
                            //anchored at top-left corner of the screen
                            Vector2.ZERO,

                            //height of border is the height of the screen
                            new Vector2(BORDER_WIDTH, windowDimensions.y()),

                            //this game object is invisible; it doesn’t have a Renderable
                            null
                    ));

        gameObjects().addGameObject(
                new GameObject(
                        //anchored at top-right corner of the screen
                        new Vector2(windowDimensions.x()-BORDER_WIDTH, 0),

                        //height of border is the height of the screen
                        new Vector2(BORDER_WIDTH, windowDimensions.y()),

                        //this game object is invisible; it doesn’t have a Renderable
                        null
                ));

        gameObjects().addGameObject(

                new GameObject(
                        //anchored at top corner of the screen
                        Vector2.ZERO,

                        //height of border is the height of the screen
                        new Vector2(windowDimensions.x() , BORDER_WIDTH),

                        //this game object is invisible; it doesn’t have a Renderable
                        null
                ));


    }

    /**
     * a constructor of BrickerGameManager class
     * @param windowTitle - window title
     * @param windowDimensions - side of the window
     */

    BrickerGameManager(String windowTitle, Vector2 windowDimensions){
        super(windowTitle, windowDimensions);
    }

    public static void main(String[] args){
        new BrickerGameManager(WINDOW_TITLE, new Vector2(WINDOE_SIZE_X, WINDOE_SIZE_Y)).run();
    }

}
