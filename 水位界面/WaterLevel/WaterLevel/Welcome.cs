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
    public partial class Welcome : Form
    {
        public static WaterLevel waterlevelForm;
        public static Display displayForm;
        public Welcome()
        {
            InitializeComponent();
            waterlevelForm = new WaterLevel();
            displayForm = new Display();
        }

        private void Welcome_Load(object sender, EventArgs e)
        {

        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            linkLabel1.LinkVisited = true;
            waterlevelForm.Show();
            this.Hide();

        }
    }
}
