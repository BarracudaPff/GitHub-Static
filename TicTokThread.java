package com.samsung.myapplication;

import android.graphics.Canvas;
import android.view.SurfaceHolder;

public class TicTokThread extends Thread {
    private final SurfaceHolder holder;

    public TicTokThread(SurfaceHolder holder) {
        this.holder = holder;
    }

    @Override
    public void run() {
        while (true) {
            Canvas canvas = holder.lockCanvas();
            // draw here
            holder.unlockCanvasAndPost(canvas);
        }
    }
}
