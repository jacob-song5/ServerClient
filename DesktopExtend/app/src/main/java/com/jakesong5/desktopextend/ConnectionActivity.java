package com.jakesong5.desktopextend;

import android.os.AsyncTask;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;

public class ConnectionActivity extends AppCompatActivity {
    private String host_addr;
    private final File download_dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
    private String current = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connection);

        TextView t = this.findViewById(R.id.results);
        t.setMovementMethod(new ScrollingMovementMethod());
        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            current = extras.getString("dir");
            host_addr = extras.getString("host_addr");
            t.setText(host_addr);
        }

        try
        {
            new AsyncLs().execute(current);
        }
        catch (Exception e)
        {
            t.setText("Not sure");
        }
    }

    public void request(View view)
    {
        EditText e = findViewById(R.id.request_entry);
        TextView t = findViewById(R.id.results);
        t.setText("Copying...");
        new AsyncCopy().execute(e.getText().toString());
    }

    private static String get_file_name(String str)
    {
        int i = str.lastIndexOf('\\');
        if (i == -1)
            return str;
        else
            return str.substring(i+1);
    }

    private class AsyncLs extends AsyncTask<String, Void, String>
    {
        private Socket connection;
        private PrintWriter out;
        private InputStreamReader in;

        @Override
        protected String doInBackground(String... args)
        {
            String msg = "";
            int n;
            char response[] = new char[250];

            try
            {
                connection = new Socket();
                connection.connect(new InetSocketAddress(host_addr, 9462), 3000);

                out = new PrintWriter(new OutputStreamWriter(connection.getOutputStream()));
                in = new InputStreamReader(connection.getInputStream());

                if (!current.equals(getString(R.string.default_dir)))
                {
                    out.print("cd " + current);
                    out.flush();
                    in.read(response, 0, 250);
                }
                out.print("ls");
                out.flush();
                for (int i = 0; i < 6; ++i)
                    in.read();
                n = in.read(response, 0,250);
                while (true)
                {
                    if (response[n-1] == '!' && response[n-2] == '!' && response[n-3] == '!' && response[n-4] == '!')
                    {
                        msg += new String(response, 0, n-5);
                        break;
                    }
                    else
                        msg += new String(response, 0, n);

                    n = in.read(response, 0, 250);
                }
                out.close();
                in.close();
                connection.close();
            }
            catch (Exception e)
            {
                return e.toString();
            }

            return msg;
        }

        @Override
        protected void onPostExecute(String result)
        {
            super.onPostExecute(result);
            TextView t = findViewById(R.id.results);
            t.setText(result);
        }
    }

    private class AsyncCopy extends AsyncTask<String, Void, String>
    {
        private Socket connection;
        private PrintWriter out;

        @Override
        protected String doInBackground(String... args)
        {
            byte[] response = new byte[512];
            String result;
            InputStream in;

            try {
                connection = new Socket();
                connection.connect(new InetSocketAddress(host_addr, 9462), 3000);

                out = new PrintWriter(new OutputStreamWriter(connection.getOutputStream()));
                in = connection.getInputStream();

                if (!current.equals(getString(R.string.default_dir))) {
                    out.print("cd " + current);
                    out.flush();
                    in.read(response, 0, 250);
                }

                out.print(args[0]);
                out.flush();

                String r = "";
                for (int i = 0; i < 6; ++i)
                    r += (char)in.read();
                if (r.equals("tr now"))
                {
                    result = "Finished";
                    File f = new File(download_dir, get_file_name(args[0]));
                    OutputStream f_out = new FileOutputStream(f);
                    int n = in.read(response, 0, 512);

                    while (n != -1)
                    {
                        f_out.write(response, 0, n);
                        n = in.read(response, 0, 512);
                    }
                    f_out.close();
                }
                else
                    result = r;

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
            TextView t = findViewById(R.id.results);
            t.setText(result);
        }
    }
}