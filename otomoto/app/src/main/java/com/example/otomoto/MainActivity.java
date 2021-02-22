package com.example.otomoto;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.pytorch.IValue;
import org.pytorch.Module;
import org.pytorch.Tensor;

public class MainActivity extends AppCompatActivity {

    private Module model;
    private TextView result;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        model = Module.load(Utils.assetFilePath(this, "model.pt"));
        setContentView(R.layout.activity_main);
        result = (TextView) findViewById(R.id.result);
        super.onCreate(savedInstanceState);
    }

    public void onClickButton(View v) {

        EditText rok = (EditText)findViewById(R.id.edit_rok);
        EditText przebieg = (EditText)findViewById(R.id.edit_przebieg);

        float rok_val = Float.parseFloat(rok.getText().toString());
        float przebieg_val = Float.parseFloat(przebieg.getText().toString());


        float[] data = {przebieg_val, rok_val};
        long[] shape = new long[]{1, data.length};
        Tensor outputTensor = model.forward(IValue.from(Tensor.fromBlob(data, shape))).toTensor();
        float[] scores = outputTensor.getDataAsFloatArray();
        result.setText(String.valueOf(scores[0]));

    }


}