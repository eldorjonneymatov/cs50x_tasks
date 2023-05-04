using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Math;
namespace simple3d
{
    public partial class MainForm : Form
    {
        int x0, y0;
        PointF O;
        Bitmap bm;
        public Graphics gr;
        int scale = 30;
        int L = 8;
        float xx, xy, xz, yx, yy, yz;
        PointF oX, oY, oZ;
        Point3D ox3, oy3, oz3;
        float alfaX, alfaY, alfaZ;
        float bb;
        bool mq = false;
        int mqn = -1;
        List<Figure> figures;
        int cubes = 0;
        int cones = 0;
        int cylinders = 0;
        int parallelepipeds = 0;
        Dictionary<string, Figure> existing_figures;
        public MainForm()
        {
            figures = new List<Figure>();
            existing_figures = new Dictionary<string, Figure>();
            InitializeComponent();
            x0 = pictureBox1.Width / 2;
            y0 = pictureBox1.Height / 2;
            O = new PointF(x0, y0);
            bb = 5;
            xx = L; yx = 0;
            xy = 0; yy = 0;
            xz = 0; yz = L;
            ox3 = new Point3D(L, 0, 0);
            oy3 = new Point3D(0, L, 0);
            oz3 = new Point3D(0, 0, L);
            drawAxes();
            alfaX = alfaY = alfaZ = 0;
            endInput();
            checkedListBox2.Location = checkedListBox1.Location;
            checkedListBox2.Size = checkedListBox1.Size;
        }
        #region buttonclick
        private void button1_Click(object sender, EventArgs e)
        {
            checkedListBox1.Visible = !checkedListBox1.Visible;
            button3.Visible = !checkedListBox1.Visible;
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (!checkedListBox2.Visible)
            {
                checkedListBox2.Items.Clear();
                foreach (var item in existing_figures)
                {
                    checkedListBox2.Items.Add(item.Key);
                }
            }
            checkedListBox2.Visible = !checkedListBox2.Visible;
            button1.Visible = !checkedListBox2.Visible;
        }
        #endregion
        private void checkedListBox1_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            if (e.CurrentValue == CheckState.Unchecked)
            {
                label9.Visible = true;
                label8.Visible = true;
                label7.Visible = true;
                textBox6.Visible = true;
                textBox5.Visible = true;
                textBox4.Visible = true;
                if (e.Index == 0)
                {
                    label6.Visible = true;
                    label6.Text = "Edge";
                    textBox3.Visible = true;
                }
                if (e.Index == 1)
                {
                    label4.Visible = true;
                    label4.Text = "Width";
                    label5.Visible = true;
                    label5.Text = "Length";
                    label6.Visible = true;
                    label6.Text = "Height";
                    textBox1.Visible = true;
                    textBox2.Visible = true;
                    textBox3.Visible = true;
                }
                if (e.Index == 2)
                {
                    label5.Visible = true;
                    label5.Text = "Base r";
                    label6.Visible = true;
                    label6.Text = "Height";
                    textBox2.Visible = true;
                    textBox3.Visible = true;
                }
                if (e.Index == 3)
                {
                    label5.Visible = true;
                    label5.Text = "Base r";
                    label6.Visible = true;
                    label6.Text = "Height";
                    textBox2.Visible = true;
                    textBox3.Visible = true;
                }
                e.NewValue = CheckState.Unchecked;
                checkedListBox1.Visible = false;
                groupBox2.Visible = true;
                button1.Visible = false;
                mqn = e.Index;
            }
        }
        private void checkedListBox2_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            if (e.CurrentValue == CheckState.Unchecked)
            {
                for (int i = 0; i < existing_figures.Count(); i++)
                {
                    if (e.Index == i)
                    {
                        figures.Remove(existing_figures[checkedListBox2.Items[e.Index].ToString()]);
                        existing_figures.Remove(checkedListBox2.Items[e.Index].ToString());
                        drawAxes();
                        break;
                    }
                }
                e.NewValue = CheckState.Unchecked;
                checkedListBox2.Visible = false;
                button1.Visible = true;
            }
        }
        private void button2_Click(object sender, EventArgs e)
        {
            if (checkValue(textBox4.Text) && checkValue(textBox5.Text) &&
                checkValue(textBox6.Text))
            {
                Point3D pnt = new Point3D(Convert.ToSingle(textBox6.Text),
                    Convert.ToSingle(textBox5.Text), Convert.ToSingle(textBox4.Text));

                if (mqn == 0)
                {
                    if (checkValueM(textBox3.Text))
                    {
                        float tedge = Convert.ToSingle(textBox3.Text);
                        mq = true;
                        figures.Add(new Parallelipepid(pnt, tedge, tedge, tedge));
                        cubes++;
                        existing_figures.Add($"Cube{cubes}", figures[figures.Count() - 1]);
                    }
                }
                else if (mqn == 1)
                {
                    if (checkValueM(textBox3.Text) && checkValueM(textBox2.Text) && checkValueM(textBox1.Text))
                    {
                        float tm1 = Convert.ToSingle(textBox1.Text);
                        float tm2 = Convert.ToSingle(textBox2.Text);
                        float tm3 = Convert.ToSingle(textBox3.Text);
                        mq = true;
                        figures.Add(new Parallelipepid(pnt, tm1, tm2, tm3));
                        parallelepipeds++;
                        existing_figures.Add($"Parallelepiped{parallelepipeds}", figures[figures.Count() - 1]);
                    }
                }
                else if (mqn == 2)
                {
                    if (checkValueM(textBox3.Text) && checkValueM(textBox2.Text))
                    {
                        float tm2 = Convert.ToSingle(textBox2.Text);
                        float tm3 = Convert.ToSingle(textBox3.Text);
                        mq = true;
                        figures.Add(new Cone(pnt, tm2, tm3));
                        cones++;
                        existing_figures.Add($"Cone{cones}", figures[figures.Count() - 1]);
                    }
                }
                else if (mqn == 3)
                {
                    if (checkValueM(textBox3.Text) && checkValueM(textBox2.Text))
                    {
                        float tm2 = Convert.ToSingle(textBox2.Text);
                        float tm3 = Convert.ToSingle(textBox3.Text);
                        mq = true;
                        figures.Add(new Silindr(pnt, tm2, tm3));
                        cylinders++;
                        existing_figures.Add($"Cylinder{cylinders}", figures[figures.Count() - 1]);
                    }
                }
            }
            if (mq)
            {
                textBox1.Text = "";
                textBox2.Text = "";
                textBox3.Text = "";
                mq = false;
                groupBox2.Visible = false;
                drawAxes();
                endInput();
            }
            else
            {
                MessageBox.Show("Incorrect information entered!");
            }
            textBox4.Text = "";
            textBox5.Text = "";
            textBox6.Text = "";
        }
        private void endInput()
        {
            textBox1.Text = "";
            textBox2.Text = "";
            textBox3.Text = "";
            textBox4.Text = "";
            textBox5.Text = "";
            textBox6.Text = "";
            label9.Visible = false;
            label8.Visible = false;
            label7.Visible = false;
            label6.Visible = false;
            label5.Visible = false;
            label4.Visible = false;
            textBox6.Visible = false;
            textBox5.Visible = false;
            textBox4.Visible = false;
            textBox3.Visible = false;
            textBox2.Visible = false;
            textBox1.Visible = false;
            groupBox2.Visible = false;
            button1.Visible = true;
            button3.Visible = true;
        }
        #region endInput
        private void label11_Click(object sender, EventArgs e)
        {
            endInput();
        }

        private void label11_MouseHover(object sender, EventArgs e)
        {
            label11.BackColor = Color.Red;
        }

        private void label11_MouseLeave(object sender, EventArgs e)
        {
            label11.BackColor = Color.White;
        }
        #endregion
        #region rotationByButtons
        private void label12_Click(object sender, EventArgs e)
        {
            alfaX = -bb;
            ox3 = rotationOx(alfaX, ox3);
            oy3 = rotationOx(alfaX, oy3);
            oz3 = rotationOx(alfaX, oz3);
            drawAxes();
        }
        private void label13_Click(object sender, EventArgs e)
        {
            alfaX = bb;
            ox3 = rotationOx(alfaX, ox3);
            oy3 = rotationOx(alfaX, oy3);
            oz3 = rotationOx(alfaX, oz3);
            drawAxes();
        }
        private void label15_Click(object sender, EventArgs e)
        {
            alfaY = -bb;
            ox3 = rotationOy(alfaY, ox3);
            oy3 = rotationOy(alfaY, oy3);
            oz3 = rotationOy(alfaY, oz3);
            drawAxes();
        }
        private void label14_Click(object sender, EventArgs e)
        {
            alfaY = bb;
            ox3 = rotationOy(alfaY, ox3);
            oy3 = rotationOy(alfaY, oy3);
            oz3 = rotationOy(alfaY, oz3);
            drawAxes();
        }
        private void label17_Click(object sender, EventArgs e)
        {
            alfaZ = -bb;
            ox3 = rotationOz(alfaZ, ox3);
            oy3 = rotationOz(alfaZ, oy3);
            oz3 = rotationOz(alfaZ, oz3);
            drawAxes();
        }
        private void label16_Click(object sender, EventArgs e)
        {
            alfaZ = bb;
            ox3 = rotationOz(alfaZ, ox3);
            oy3 = rotationOz(alfaZ, oy3);
            oz3 = rotationOz(alfaZ, oz3);
            drawAxes();
        }
        #endregion
        #region cursor
        private void label12_MouseHover(object sender, EventArgs e)
        {
            Cursor = Cursors.Hand;
        }

        private void label13_MouseHover(object sender, EventArgs e)
        {
            Cursor = Cursors.Hand;
        }

        private void label15_MouseHover(object sender, EventArgs e)
        {
            Cursor = Cursors.Hand;
        }

        private void label14_MouseHover(object sender, EventArgs e)
        {
            Cursor = Cursors.Hand;
        }

        private void label17_MouseHover(object sender, EventArgs e)
        {
            Cursor = Cursors.Hand;
        }

        private void label16_MouseHover(object sender, EventArgs e)
        {
            Cursor = Cursors.Hand;
        }

        private void label12_MouseLeave(object sender, EventArgs e)
        {
            Cursor = Cursors.Default;
        }
        private void label13_MouseLeave(object sender, EventArgs e)
        {
            Cursor = Cursors.Default;
        }

        private void label15_MouseLeave(object sender, EventArgs e)
        {
            Cursor = Cursors.Default;
        }

        private void label14_MouseLeave(object sender, EventArgs e)
        {
            Cursor = Cursors.Default;
        }

        private void label17_MouseLeave(object sender, EventArgs e)
        {
            Cursor = Cursors.Default;
        }

        private void label16_MouseLeave(object sender, EventArgs e)
        {
            Cursor = Cursors.Default;
        }

        #endregion
        #region inputKeydown
        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Down) textBox2.Select();
        }

        private void textBox2_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Down) textBox3.Select();
        }

        private void textBox3_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Down) textBox6.Select();
        }

        private void textBox6_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Down) textBox5.Select();
        }

        private void textBox5_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Down) textBox4.Select();
        }

        private void textBox4_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Down) button2.Select();
        }
        #endregion
        #region inputForecolor
        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            if (!checkValueM(textBox1.Text)) textBox1.ForeColor = Color.Red;
            else textBox1.ForeColor = Color.Black;
        }
        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            if (!checkValueM(textBox2.Text)) textBox2.ForeColor = Color.Red;
            else textBox2.ForeColor = Color.Black;
        }
        private void textBox3_TextChanged(object sender, EventArgs e)
        {
            if (!checkValueM(textBox3.Text)) textBox3.ForeColor = Color.Red;
            else textBox3.ForeColor = Color.Black;
        }
        private void textBox4_TextChanged(object sender, EventArgs e)
        {
            if (!checkValue(textBox4.Text)) textBox4.ForeColor = Color.Red;
            else textBox4.ForeColor = Color.Black;
        }
        private void textBox5_TextChanged(object sender, EventArgs e)
        {
            if (!checkValue(textBox5.Text)) textBox5.ForeColor = Color.Red;
            else textBox5.ForeColor = Color.Black;
        }
        private void textBox6_TextChanged(object sender, EventArgs e)
        {
            if (!checkValue(textBox6.Text)) textBox6.ForeColor = Color.Red;
            else textBox6.ForeColor = Color.Black;
        }
        #endregion
        private bool checkValue(string s)
        {
            try
            {
                float tf = Convert.ToSingle(s);
                if (tf < -8 || tf > 8) return false;
                else return true;
            }
            catch
            {
                return false;
            }
        }
        private bool checkValueM(string s)
        {
            try
            {
                float tf = Convert.ToSingle(s);
                if (tf <= 0 || tf > 8) return false;
                else return true;
            }
            catch
            {
                return false;
            }
        }
        private PointF changeCoordinate(PointF p)
        {
            return new PointF(x0 + p.X * scale, y0 - p.Y * scale);
        }
        private PointF convertPoint(Point3D n)
        {
            PointF tp = new PointF((n.X * L + n.Y * 0 + n.Z * 0) / L, (n.X * 0 + n.Y * 0 + n.Z * L) / L);
            return changeCoordinate(tp);
        }
        private void drawAxes()
        {
            Clear();
            oX = convertPoint(ox3);
            oY = convertPoint(oy3);
            oZ = convertPoint(oz3);
            Pen pen = new Pen(Color.Blue, 2);
            gr.DrawLine(pen, O, oX);
            gr.DrawLine(new Pen(Color.Red, 2), O, oY);
            gr.DrawLine(new Pen(Color.Green, 2), O, oZ);
            xx = (oX.X - x0) / scale;
            yx = (-oX.Y + y0) / scale;
            xy = (oY.X - x0) / scale;
            yy = (-oY.Y + y0) / scale;
            xz = (oZ.X - x0) / scale;
            yz = (-oZ.Y + y0) / scale;
            foreach (var item in figures)
            {
                item.Draw(xx, xy, xz, yx, yy, yz, L, x0, y0, scale, gr);
            }
        }

        private void MainForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Right)
            {
                alfaX = -bb;
                ox3 = rotationOx(alfaX, ox3);
                oy3 = rotationOx(alfaX, oy3);
                oz3 = rotationOx(alfaX, oz3);
                drawAxes();
            }
            else if (e.KeyCode == Keys.Left)
            {
                alfaX = bb;
                ox3 = rotationOx(alfaX, ox3);
                oy3 = rotationOx(alfaX, oy3);
                oz3 = rotationOx(alfaX, oz3);
                drawAxes();
            }
            else if (e.KeyCode == Keys.Up)
            {
                alfaY = -bb;
                ox3 = rotationOy(alfaY, ox3);
                oy3 = rotationOy(alfaY, oy3);
                oz3 = rotationOy(alfaY, oz3);
                drawAxes();
            }
            else if (e.KeyCode == Keys.Down)
            {
                alfaY = bb;
                ox3 = rotationOy(alfaY, ox3);
                oy3 = rotationOy(alfaY, oy3);
                oz3 = rotationOy(alfaY, oz3);
                drawAxes();
            }
            if (e.KeyCode == Keys.Q)
            {
                alfaZ = -bb;
                ox3 = rotationOz(alfaZ, ox3);
                oy3 = rotationOz(alfaZ, oy3);
                oz3 = rotationOz(alfaZ, oz3);
                drawAxes();
            }
            else if (e.KeyCode == Keys.W)
            {
                alfaZ = bb;
                ox3 = rotationOz(alfaZ, ox3);
                oy3 = rotationOz(alfaZ, oy3);
                oz3 = rotationOz(alfaZ, oz3);
                drawAxes();
            }
        }
        private void Clear()
        {
            bm = new Bitmap(2 * x0, 2 * y0);
            pictureBox1.Image = bm;
            gr = Graphics.FromImage(pictureBox1.Image);
            gr.Clear(Color.White);
        }
        #region rotation
        private Point3D rotationOx(float al, Point3D n)
        {
            double alfa = al * PI / 180;
            Point3D nn = new Point3D(0, 0, 0);
            nn.X = n.X;
            nn.Y = (float)(n.Y * Cos(alfa) - n.Z * Sin(alfa));
            nn.Z = (float)(n.Y * Sin(alfa) + n.Z * Cos(alfa));
            return nn;
        }
        private Point3D rotationOy(float al, Point3D n)
        {
            double alfa = al * PI / 180;
            Point3D nn = new Point3D(0, 0, 0);
            nn.Y = n.Y;
            nn.X = (float)(n.X * Cos(alfa) + n.Z * Sin(alfa));
            nn.Z = (float)(-n.X * Sin(alfa) + n.Z * Cos(alfa));
            return nn;
        }
        private Point3D rotationOz(float al, Point3D n)
        {
            double alfa = al * PI / 180;
            Point3D nn = new Point3D(0, 0, 0);
            nn.Z = n.Z;
            nn.X = (float)(n.X * Cos(alfa) - n.Y * Sin(alfa));
            nn.Y = (float)(n.X * Sin(alfa) + n.Y * Cos(alfa));
            return nn;
        }
        #endregion
        #region off
        private void offLabel_MouseHover(object sender, EventArgs e)
        {
            offLabel.BackColor = Color.Red;
        }

        private void offLabel_MouseLeave(object sender, EventArgs e)
        {
            offLabel.BackColor = Color.White;
        }

        private void offLabel_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }
        #endregion
    }
}
