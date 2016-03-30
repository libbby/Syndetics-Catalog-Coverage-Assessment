#!/usr/bin/perl
use strict;
use warnings;
use DBI;
use  DBD::Oracle;
use utf8;
use locale;
use Net::SSH2;
use Getopt::Long; #allows for use of testing mode, http://perldoc.perl.org/Getopt/Long.html

# set character encoding for stdout to utf8
binmode(STDOUT, ":utf8");

#************************************************************************************
# Set up environment and make sure it is clean
#************************************************************************************
$ENV{'PATH'} = '/bin:/usr/sbin';
delete @ENV{'ENV', 'BASH_ENV'};
$ENV{'NLS_LANG'} = 'AMERICAN_AMERICA.AL32UTF8';

#############################################
# set testing mode from command line arguments
#############################################
my $testing = '';
GetOptions ('testing' => \$testing);

#************************************************************************************
# Set up database stuff
#************************************************************************************
my($dbh, $sth, $sql);

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

my $all_rows = 0;
my @collrows = <COLLS>;
foreach my $coll (@collrows) {
    my $coll_ct = 0;
    chomp $coll;
    my ($coll_query, $coll_code) = split(/\t/, $coll);

    print "Compiling list of unsuppressed records in collection: $coll_query...";
    # get the relevant MARC fields
    my $sth = $dbh->prepare( "
   SELECT v.rec_key
        FROM var_fields2 v
        INNER JOIN biblio2base b
        ON v.rec_key = b.rec_key
          AND b.bcode3 NOT IN ('d', 'n', 'c')
        WHERE marc_tag = '773'
        AND rec_data LIKE '|t${coll_query}%'
");

    $sth->execute();

    my $bnum;
    $sth->bind_columns( undef, \$bnum);

    while ($sth->fetch()) {
        print OUTFILE "$coll_code,$bnum,$bnum$coll_code\n";
        $coll_ct += 1;
    }
    print " Found $coll_ct records.\n";
    $all_rows += $coll_ct;

    $sth->finish();
}

$dbh->disconnect();
close(COLLS);
close(OUTFILE);
print "Total records identified: $all_rows\n";
exit;
