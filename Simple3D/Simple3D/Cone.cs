using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using static System.Math;
namespace simple3d
{
    class Cone : Figure
    {
        private Point3D A { get; set; }
        private float R { get; set; }
        private float H { get; set; }
        private Graphics g { get; set; }
        Pen pen = new Pen(Color.LightPink, 7);
        Pen pen2 = new Pen(Color.HotPink, 3);
        public Cone(Point3D A, float r, float h)
        {
            this.A = A;
            this.R = r;
            this.H = h;
        }

        public override void Draw(float xx, float xy, float xz, float yx, float yy, float yz, float L, float x0, float y0, float scale, Graphics g)
        {
            this.g = g;
            float[] xs = new float[10] { xx, xy, xz, yx, yy, yz, L, x0, y0, scale };
            Point3D n = new Point3D(A.X, A.Y, A.Z + H);
            float alfa = 0;
            List<PointF> points1 = new List<PointF>();
            List<PointF> points2 = new List<PointF>();
            while (alfa <= 4 * PI + 0.2)
            {
                points1.Add(convertPoint(new Point3D((float)(A.X + R * Sin(alfa)), (float)(A.Y - R * Cos(alfa)), A.Z), xs));
                g.DrawLine(pen, convertPoint(new Point3D((float)(A.X + R * Sin(alfa)), (float)(A.Y - R * Cos(alfa)), A.Z), xs),
                convertPoint(n, xs));
                g.DrawLine(pen, convertPoint(new Point3D((float)(A.X + R * Sin(alfa)), (float)(A.Y - R * Cos(alfa)), A.Z), xs),
                convertPoint(new Point3D((float)(A.X + R * Sin(alfa + PI)), (float)(A.Y - R * Cos(alfa + PI)), A.Z), xs));
                alfa += 0.04f;
            }
            g.DrawLines(pen2, points1.ToArray());
        }
    }
}
