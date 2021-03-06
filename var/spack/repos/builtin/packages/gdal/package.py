from spack import *

class Gdal(Package):
    """
    GDAL is a translator library for raster and vector geospatial
    data formats that is released under an X/MIT style Open Source
    license by the Open Source Geospatial Foundation. As a library,
    it presents a single raster abstract data model and vector
    abstract data model to the calling application for all supported
    formats. It also comes with a variety of useful command line
    utilities for data translation and processing
    """

    homepage   = "http://www.gdal.org/"
    url        = "http://download.osgeo.org/gdal/2.0.2/gdal-2.0.2.tar.gz"
    list_url   = "http://download.osgeo.org/gdal/"
    list_depth = 2

    version('2.0.2', '573865f3f59ba7b4f8f4cddf223b52a5')

    extends('python')

    variant('hdf5', default=False, description='Enable HDF5 support')
    variant('hdf', default=False, description='Enable HDF4 support')
    variant('openjpeg', default=False, description='Enable JPEG2000 support')
    variant('geos', default=False, description='Enable GEOS support')
    variant('kea', default=False, description='Enable KEA support')
    variant('netcdf', default=False, description='Enable netcdf support')

    depends_on('swig')
    depends_on("hdf5", when='+hdf5')
    depends_on("hdf", when='+hdf')
    depends_on("openjpeg", when='+openjpeg')
    depends_on("geos", when='+geos')
    depends_on("kealib", when='+kea')
    depends_on("netcdf", when='+netcdf')
    depends_on("libtiff")
    depends_on("libpng")
    depends_on("zlib")
    depends_on("proj")
    depends_on("py-numpy")

    parallel = False

    def install(self, spec, prefix):
        args = []
        args.append("--prefix=%s" % prefix)
        args.append("--with-liblzma=yes")
        args.append("--with-zlib=%s" % spec['zlib'].prefix)
        args.append("--with-python=%s" % spec['python'].prefix.bin + "/python")
        args.append("--without-libtool")

        if '+geos' in spec:
            args.append('--with-geos=yes')
        if '+hdf' in spec:
            args.append('--with-hdf4=%s' % spec['hdf'].prefix)
        if '+hdf5' in spec:
            args.append('--with-hdf5=%s' % spec['hdf5'].prefix)
        if '+openjpeg' in spec:
            args.append('--with-openjpeg=%s' % spec['openjpeg'].prefix)
        if '+kea' in spec:
            args.append('--with-kea=yes')
        if '+netcdf' in spec:
            args.append('--with-netcdf=%s' % spec['netcdf'].prefix)

        configure(*args)

        make()
        make("install")
