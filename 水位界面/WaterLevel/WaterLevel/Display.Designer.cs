namespace WaterLevel
{
    partial class Display
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Display));
            this.button1 = new System.Windows.Forms.Button();
            this.dispTextBox1 = new System.Windows.Forms.RichTextBox();
            this.chosItem = new System.Windows.Forms.ComboBox();
            this.axWindowsMediaPlayer1 = new AxWMPLib.AxWindowsMediaPlayer();
            ((System.ComponentModel.ISupportInitialize)(this.axWindowsMediaPlayer1)).BeginInit();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(67, 980);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(320, 72);
            this.button1.TabIndex = 0;
            this.button1.Text = "载入";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // dispTextBox1
            // 
            this.dispTextBox1.Location = new System.Drawing.Point(67, 163);
            this.dispTextBox1.Name = "dispTextBox1";
            this.dispTextBox1.Size = new System.Drawing.Size(526, 640);
            this.dispTextBox1.TabIndex = 1;
            this.dispTextBox1.Text = "";
            // 
            // chosItem
            // 
            this.chosItem.FormattingEnabled = true;
            this.chosItem.Items.AddRange(new object[] {
            "西工商河",
            "东工商河"});
            this.chosItem.Location = new System.Drawing.Point(67, 868);
            this.chosItem.Name = "chosItem";
            this.chosItem.Size = new System.Drawing.Size(320, 32);
            this.chosItem.TabIndex = 3;
            this.chosItem.Text = "（请选择）";
            // 
            // axWindowsMediaPlayer1
            // 
            this.axWindowsMediaPlayer1.Enabled = true;
            this.axWindowsMediaPlayer1.Location = new System.Drawing.Point(600, 76);
            this.axWindowsMediaPlayer1.Name = "axWindowsMediaPlayer1";
            this.axWindowsMediaPlayer1.OcxState = ((System.Windows.Forms.AxHost.State)(resources.GetObject("axWindowsMediaPlayer1.OcxState")));
            this.axWindowsMediaPlayer1.Size = new System.Drawing.Size(720, 680);
            this.axWindowsMediaPlayer1.TabIndex = 4;
            // 
            // Display
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 24F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1894, 1009);
            this.Controls.Add(this.axWindowsMediaPlayer1);
            this.Controls.Add(this.chosItem);
            this.Controls.Add(this.dispTextBox1);
            this.Controls.Add(this.button1);
            this.Name = "Display";
            this.Text = "Display";
            ((System.ComponentModel.ISupportInitialize)(this.axWindowsMediaPlayer1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.RichTextBox dispTextBox1;
        private System.Windows.Forms.ComboBox chosItem;
        private AxWMPLib.AxWindowsMediaPlayer axWindowsMediaPlayer1;
    }
}