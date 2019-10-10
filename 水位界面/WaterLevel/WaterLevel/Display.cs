using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;

namespace WaterLevel
{
    public partial class Display : Form
    {
        string FILE_PATH = "D:/C#_finial/gaugeReader.log";
        string MEDIA_PATH_1 = "D:/C#_finial/water_gauge_pooling/格式工厂西工商河-北园桥_2019070611355124AFD6A0_1562384151_1.mp4";
        string MEDIA_PATH_2 = "D:/C#_finial/water_gauge_pooling/东工商河-北园桥_2019070611372824AFD6A0_1562384248_1 00_00_20-00_00_50.mp4";

        string PYTHON_PATH = "D:/C#_finial/gaugeReader_v0.1.py";
        //string PYTHON_PATH = "D:/1130test/test.py";
        string mode = "00";
        public Display()
        {
            InitializeComponent();
            this.WindowState = FormWindowState.Maximized;
        }

        private void button1_Click(object sender, EventArgs e)
        {

            if (chosItem.Text == "西工商河")
            {
                axWindowsMediaPlayer1.URL = (MEDIA_PATH_1);
                axWindowsMediaPlayer1.Ctlcontrols.play();
                mode = "01\r\n";
            }
            if (chosItem.Text == "东工商河")
            {
                axWindowsMediaPlayer1.URL = (MEDIA_PATH_2);
                axWindowsMediaPlayer1.Ctlcontrols.play();
                mode = "02\r\n";
            }

            if (mode == "00")
                return;

            button1.Text = "Loading...";

            System.Diagnostics.Process cmd = new System.Diagnostics.Process();
            cmd.StartInfo.FileName = "C:/Program Files/Anaconda3/python.exe";
            cmd.StartInfo.UseShellExecute = false;
            cmd.StartInfo.RedirectStandardInput = true;
            cmd.StartInfo.RedirectStandardOutput = false;
            cmd.StartInfo.CreateNoWindow = false;
            cmd.StartInfo.Arguments = PYTHON_PATH;
            cmd.Start();

            cmd.StandardInput.WriteLine(mode + "&exit");
            cmd.StandardInput.AutoFlush = true;
            cmd.WaitForExit();
            cmd.Close();

            button1.Text = "载入";

            try
            {
                StreamReader doc = new StreamReader(FILE_PATH);
                string line;
                dispTextBox1.Text = "";
                while ((line = doc.ReadLine()) != null)
                {
                    dispTextBox1.Text = dispTextBox1.Text + line + '\r' + '\n';
                }
                doc.Close();
            }
            catch(Exception ex)
            {
                MessageBox.Show("有个傻逼正在占用");
            }
            
        }

        private void axWindowsMediaPlayer1_Enter(object sender, EventArgs e)
        {
            
        }
    }
}
