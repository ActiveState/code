private static Vector3 SurfaceNormal(Vector3 c1, Vector3 c2, Vector3 c3)
{
    Vector3 edge1 = new Vector3(c2.X - c1.X, c2.Y - c1.Y, c2.Z - c1.Z);
    Vector3 edge2 = new Vector3(c3.X - c1.X, c3.Y - c1.Y, c3.Z - c1.Z);

    Vector3 normal = Vector3.Cross(edge1, edge2);
    normal.Normalize();

    return normal;
}
