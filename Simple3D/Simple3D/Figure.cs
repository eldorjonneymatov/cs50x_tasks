using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
namespace simple3d
{
    class Figure
    {
        public virtual void Draw(float xx, float xy, float xz, float yx, float yy, float yz, float L, float x0,float y0, float scale, Graphics g) { }
        protected PointF convertPoint(Nuqta3D n, float[] f)
        {
            PointF tp = new PointF((n.X * f[0] + n.Y * f[1] + n.Z * f[2]) / f[6], (n.X * f[3] + n.Y * f[4] + n.Z * f[5]) / f[6]);
            return changeCoordinate(tp,f[7],f[8],f[9]);
        }
        private PointF changeCoordinate(PointF p,float x0,float y0,float scale)
        {
            return new PointF(x0 + p.X * scale, y0 - p.Y * scale);
        }
    }
}
