#!/usr/bin/perl -I/home/phil/perl/cpan/DataTableText/lib/
#-------------------------------------------------------------------------------
# Use pycco to create some documentation
# Philip R Brenan at gmail dot com, Appa Apps Ltd Inc., 2020
#-------------------------------------------------------------------------------
use warnings FATAL => qw(all);
use strict;
use Carp;
use Data::Dump qw(dump);
use Data::Table::Text qw(:all);

my $home    = q(/home/phil/vita/vitaCore/);                                     # Home folder
my $modules = fpd($home, qw(vita modules));                                     # Modules folder
my $docs    = fpd($home, q(docs));                                              # Output documentation

my @errors;

makePath($docs);
clearFolder($docs, 99);

my @files = searchDirectoryTreesForMatchingFiles($modules, qw(.py));            # Modules to document

#say STDERR qx(/home/phil/.local/bin/pycco -d $docs -ie $files);

for my $source(@files)
 {say STDERR $source;
  my $target = fpe($docs, fn($source), q(html));
  my $r = extractPythonDocumentation($source, $target);
  push @errors, $r->errors->@*;
 }

owf(fpe($docs, qw(aaaErrors txt)), join "\n", @errors);
