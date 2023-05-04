using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
namespace simple3d
{
    class Parallelepiped: Figure
    {
        private Point3D A { get; set; }
        private float a { get; set; }
        private float b { get; set; }
        private float c { get; set; }
        private Graphics g { get; set; }
        private Point3D B, C, D, A1, B1, C1, D1;
        public Parallelepiped(Point3D A,float a,float b,float c)
        {
            this.A = A;
            this.a = a;
            this.b = b;
            this.c = c;
            this.B = new Point3D(A.X, A.Y, A.Z + c);
            this.C = new Point3D(A.X + a, A.Y, A.Z + c);
            this.D = new Point3D(A.X + a, A.Y, A.Z);
            this.A1 = new Point3D(A.X, A.Y + b, A.Z);
            this.B1 = new Point3D(A.X, A.Y + b, A.Z + c);
            this.C1 = new Point3D(A.X + a, A.Y + b, A.Z + c);
            this.D1 = new Point3D(A.X + a, A.Y + b, A.Z);
        }
        private void drawRectangle(Graphics g, Point3D n1, Point3D n2, Point3D n3, Point3D n4,float[] xs)
        {
            g.DrawPolygon(new Pen(Color.Black, 2), new PointF[] { convertPoint(n1,xs), convertPoint(n2,xs), convertPoint(n3,xs), convertPoint(n4,xs) });
        }
        public override void Draw(float xx, float xy, float xz, float yx, float yy, float yz, float L, float x0, float y0, float scale, Graphics g)
        {

            this.g = g;
            float[] xs = new float[10] { xx, xy, xz, yx, yy, yz, L, x0, y0, scale };
            drawRectangle(g, A, B, C, D, xs);
            drawRectangle(g, A, B, B1, A1, xs);
            drawRectangle(g, B, C, C1, B1, xs);
            drawRectangle(g, A1, B1, C1, D1, xs);
            drawRectangle(g, A, D, D1, A1, xs);
            drawRectangle(g, C, D, D1, C1, xs);
        }
    }
}
