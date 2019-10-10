using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WaterLevel
{
    public partial class WaterLevel : Form
    {
        public WaterLevel()
        {
            InitializeComponent();
           this.BackgroundImage = Image.FromFile("C:/Users/stone/Desktop/水位界面/back.png");
            this.Size = this.BackgroundImage.Size;
        }

        private void myDefaultBtn_Click(object sender, EventArgs e)
        {
            if (tbxUsr.Text == string.Empty || tbxPwd.Text == string.Empty)
            {
                MessageBox.Show("信息不完整！", "提示");
                return;
            }
            if (!tbxUsr.Text.Equals("123") || !tbxPwd.Text.Equals("123"))
            {
                MessageBox.Show("用户名或密码不正确！", "提示");
            }
            else
            {
                Welcome.displayForm.Show();
                this.Close();
            }
        }

        private void WaterLevel_Load(object sender, EventArgs e)
        {

        }
    }
}
