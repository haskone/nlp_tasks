#!/usr/bin/perl -w -CAS
use utf8;
use strict;
use warnings;

my $num_args = $#ARGV + 1;
if ($num_args != 1) {
    print "Usage: filter.pl path/to/text.txt\n";
    exit;
}

my $filename = $ARGV[0];
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";

while (my $line = <$fh>) {
    $line =~ s/[[:punct:]]//g;
    $line = lc($line);
    $line =~ s/\d+//g;
    $line =~ s/[a-z]+//g;
    $line =~ s/\n/ /g;
    $line =~ s/\s{2,}/ /g;
    print $line;
}

close($fh)
    or die "Could not close file '$filename' $!";
