#!/usr/bin/perl

# See the following link for documentation on this script:
# https://github.com/UNC-Libraries/Syndetics-Catalog-Coverage-Assessment

use strict;
use warnings;
use DBI;
use  DBD::Oracle;
use utf8;
use locale;
use Net::SSH2;

# set character encoding for stdout to utf8
binmode(STDOUT, ":utf8");

#************************************************************************************
# Set up environment and make sure it is clean
#************************************************************************************
$ENV{'PATH'} = '/bin:/usr/sbin';
delete @ENV{'ENV', 'BASH_ENV'};
$ENV{'NLS_LANG'} = 'AMERICAN_AMERICA.AL32UTF8';

#************************************************************************************
# Set up database stuff
#************************************************************************************
my($dbh, $sql);

my $input = '/htdocs/connects/afton_iii_iiidba_perl.inc';
my @pair;
my %mycnf;

open (DBFILE, "<$input") || die &mail_error("Can't open hidden file\n");
  while (<DBFILE>){
    chomp;
    @pair = split("=", $_);
    $mycnf{$pair[0]} = $pair[1];
  }

close(DBFILE);

my $host = $mycnf{"host"};
my $sid = $mycnf{"sid"};
my $username = $mycnf{"user"};
my $password = $mycnf{"password"};

# untaint all of the db connection variables
if ($host =~ /^([-\@\w.]+)$/) {
     $host=$1;
} else {
     die "Bad data in $host";
}

if ($sid =~ /^([-\@\w.]+)$/) {
     $sid=$1;
} else {
     die "Bad data in $sid";
}

if ($username =~ /^([-\@\w.]+)$/) {
     $username=$1;
} else {
     die "Bad data in $username";
}

$dbh = DBI->connect("dbi:Oracle:host=$host;sid=$sid", $username, $password)
        or die &mail_error("Unable to connect: $DBI::errstr");

# So we don't have to check every DBI call we set RaiseError.
$dbh->{RaiseError} = 1;

#############################################
# $coll_list should be a .txt file, consisting of one collection per line.
# The format is tab delimited. First, the collection name (from 773).
#  The expectation is that it should be a left-anchored exact match search, but right/end of string is open-ended
# After the tab, a shorthand code for the collection.

# The following bit of code grabs the collection info and prepares it for querying the DB and writing results.
#############################################
my $coll_list = $ARGV[0];
my $output_file = $coll_list;

$output_file =~ s/\.txt$/_bibs.csv/;

open(COLLS, "<:utf8", "$coll_list") or die "Couldn't open input file given: $coll_list\n";
open(OUTFILE, ">:utf8", "$output_file") or die "Couldn't open $output_file for output: $!\n";

my @collrows = <COLLS>;
my %collhash; #773 value and coll code
my %collct; #number of records found for each collection

foreach my $coll (@collrows) {
    chomp $coll;
    my ($coll_query, $coll_code) = split(/\t/, $coll);
    $collhash{$coll_query} = $coll_code;
};
close(COLLS);

foreach my $collstr1 (keys %collhash) {
    $collct{$collstr1} = 0;
}

# get the relevant MARC fields
my $sth = $dbh->prepare( "
   SELECT v.rec_key, v.rec_data
        FROM var_fields2 v
        INNER JOIN biblio2base b
        ON v.rec_key = b.rec_key
          AND b.bcode3 NOT IN ('d', 'n', 'c')
          AND b.mat_type IN ('z', 'g', 'j', 'w', 's')
        WHERE marc_tag = '773'
        AND rec_data LIKE '%(online collection)%'
");

$sth->execute();

my ($bnum, $rec_data);
$sth->bind_columns( undef, \$bnum, \$rec_data);

while ($sth->fetch()) {
    $rec_data =~ s/^\|t//;
    foreach my $collstr2 (keys %collhash) {
        if (index($rec_data, $collstr2) == 0) {
            print OUTFILE "$collhash{$collstr2},$bnum,$collhash{$collstr2}$bnum\n";
            $collct{$collstr2} += 1;
        }
    }
}

$sth->finish();
$dbh->disconnect();
close(OUTFILE);

my $all_rows = 0;
foreach my $collstr3 (keys %collct) {
    print "$collct{$collstr3} recs : $collstr3\n";
    $all_rows += $collct{$collstr3};
}

print "Total records identified: $all_rows\n";
exit;
