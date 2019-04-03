package com.jakesong5.desktopextend;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    private String host_addr;
    private Bundle b = new Bundle();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        int REQUEST_CODE_ASK_PERMISSIONS = 123;
        host_addr = "192.168.0.17";
        b.putString("host_addr", host_addr);

        int hasWriteFilePermission = checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE);
        if (hasWriteFilePermission != PackageManager.PERMISSION_GRANTED)
            requestPermissions(new String[] {Manifest.permission.WRITE_EXTERNAL_STORAGE}, REQUEST_CODE_ASK_PERMISSIONS);
    }

    public void set_host_addr(View view)
    {
        EditText e = findViewById(R.id.host_addr_entry);
        String r = e.getText().toString();
        if (r.length() > 0) {
            host_addr = r;
            b.putString("host_addr", host_addr);
        }

        TextView t = findViewById(R.id.host_label);
        t.setText("Address of Server: " + r);
    }

    public void sendLs(View view)
    {
        Intent ls = new Intent(MainActivity.this, ConnectionActivity.class);
        TextView t = findViewById(R.id.current_dir);
        b.putString("dir", t.getText().toString());
        ls.putExtras(b);
        startActivity(ls);
    }

    public void sendCd(View view)
    {
        TextView t = findViewById(R.id.current_dir);
        EditText e = findViewById(R.id.entry_field);
        String path = e.getText().toString();
        String cur = t.getText().toString();

        if (improperPath(path))
            (new Async_cd()).execute(cur, childPath(cur, path));

        else if (path != "")
            (new Async_cd()).execute(cur, path);
    }

    public void sendBackCd(View view)
    {
        TextView t = findViewById(R.id.current_dir);
        String cur = t.getText().toString();
        if (!isRoot(cur))
            (new Async_cd()).execute(cur, parentPath(cur));
    }

    private class Async_cd extends AsyncTask<String, Void, String>
    {
        private Socket connection;
        private PrintWriter out;
        private InputStreamReader in;

        @Override
        protected String doInBackground(String... args)
        {
            String old_path = args[0];
            String request = args[1];
            String result;
            int n;
            char[] response = new char[100];


            try
            {
                connection = new Socket();
                connection.connect(new InetSocketAddress(host_addr, 9462), 3000);

                out = new PrintWriter(new OutputStreamWriter(connection.getOutputStream()));
                in = new InputStreamReader(connection.getInputStream());
                out.print("cd " + request);
                out.flush();

                n = in.read(response, 0, 100);
                String r = new String(response, 0, n);
                if (r.equals("path changed"))
                    result = request;
                else
                    result = old_path;

                in.close();
                out.close();
                connection.close();
                return result;
            }

            catch (Exception e)
            {
                return e.toString();
            }
        }

        @Override
        protected void onPostExecute(String result)
        {
            super.onPostExecute(result);
            TextView t = findViewById(R.id.current_dir);
            t.setText(result);
            EditText e = findViewById(R.id.entry_field);
            e.setText("");
        }
    }

    private boolean isRoot(String str)
    {
        return (str.indexOf('\\') == -1);
    }

    private String parentPath(String str)
    {
        return str.substring(0, str.lastIndexOf('\\'));
    }

    private String childPath(String parent, String str)
    {
        return parent + '\\' + str;
    }

    private boolean improperPath(String str)
    {
        return (str.indexOf('\\') == -1) && (str.indexOf(':') == -1);
    }
}