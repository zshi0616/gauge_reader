namespace WaterLevel
{
    partial class WaterLevel
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
            this.tbxPwd = new System.Windows.Forms.TextBox();
            this.tbxUsr = new System.Windows.Forms.TextBox();
            this.myDefaultBtn = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // tbxPwd
            // 
            this.tbxPwd.Location = new System.Drawing.Point(774, 570);
            this.tbxPwd.Multiline = true;
            this.tbxPwd.Name = "tbxPwd";
            this.tbxPwd.PasswordChar = '*';
            this.tbxPwd.Size = new System.Drawing.Size(166, 40);
            this.tbxPwd.TabIndex = 2;
            // 
            // tbxUsr
            // 
            this.tbxUsr.Location = new System.Drawing.Point(774, 475);
            this.tbxUsr.Multiline = true;
            this.tbxUsr.Name = "tbxUsr";
            this.tbxUsr.Size = new System.Drawing.Size(166, 40);
            this.tbxUsr.TabIndex = 3;
            // 
            // myDefaultBtn
            // 
            this.myDefaultBtn.Font = new System.Drawing.Font("宋体", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.myDefaultBtn.Location = new System.Drawing.Point(1019, 518);
            this.myDefaultBtn.Name = "myDefaultBtn";
            this.myDefaultBtn.Size = new System.Drawing.Size(108, 59);
            this.myDefaultBtn.TabIndex = 5;
            this.myDefaultBtn.Text = "登录";
            this.myDefaultBtn.UseVisualStyleBackColor = true;
            this.myDefaultBtn.Click += new System.EventHandler(this.myDefaultBtn_Click);
            // 
            // WaterLevel
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.ClientSize = new System.Drawing.Size(1239, 647);
            this.Controls.Add(this.myDefaultBtn);
            this.Controls.Add(this.tbxUsr);
            this.Controls.Add(this.tbxPwd);
            this.Name = "WaterLevel";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "WaterLevel";
            this.Load += new System.EventHandler(this.WaterLevel_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.TextBox tbxPwd;
        private System.Windows.Forms.TextBox tbxUsr;
        private System.Windows.Forms.Button myDefaultBtn;
    }
}