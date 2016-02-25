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
# Set up files and locations
#############################################
my $input_file = $ARGV[0];
my $output_file = $input_file;

$output_file =~ s/\.csv$/_final.csv/;

open(INFILE, "<:utf8", "$input_file") or die "Couldn't open input file given: $input_file\n";
open(OUTFILE, ">:utf8", "$output_file") or die "Couldn't open $output_file for output: $!\n";

my $header = <INFILE>;
chomp $header;
my $newheader = $header . ",LC CLASS BOOL,LCSH COUNT,MESH COUNT,OTHER SH COUNT\n";
print OUTFILE $newheader;

my @datarows = <INFILE>;

foreach my $row (@datarows) {
    chomp $row;
    # set/reset counter variables
    my $lc_cn = 0;
    my $lcsh_ct = 0;
    my $mesh_ct = 0;
    my $o_sh_ct = 0;

    # isolate the bnum
    my $bnum = $row;
    $bnum =~ s/^.*?,[A-Z]+(b\d+),.*$/$1/;

    # get the relevant MARC fields
    my $sth = $dbh->prepare(<<SQL);
    select marc_tag,
        indicator1,
        indicator2,
        rec_data
        from var_fields2
        where rec_key = '$bnum'
        and (marc_tag in ('050','090') OR marc_tag like '6%')
SQL

$sth->execute();

my ($tag, $i1, $i2, $data);
$sth->bind_columns( undef, \$tag, \$i1, \$i2, \$data);

print "\n\nRetrieving relevant MARC data for $bnum...\n";
    while ($sth->fetch()) {
        print "$tag  $i1$i2$data\n";

        if ($tag =~ /0[59]0/) {
            if ($data =~ /\^|a[A-Z]{1,3}\d+/) {
                $lc_cn = 1;
            }
        }
        elsif ($tag =~ /^6/) {
            if ($i2 eq "0") {
                $lcsh_ct += 1;
            }
            elsif ($i2 eq "2") {
                $mesh_ct += 1;
            }
            else {
                $o_sh_ct += 1 unless ($data =~ /\|2fast/);
            }
        }
    }

    $row .= ",$lc_cn,$lcsh_ct,$mesh_ct,$o_sh_ct\n";
    print OUTFILE $row;

# close statement handle, database handle, and output file.
$sth->finish();
}

$dbh->disconnect();

exit;
